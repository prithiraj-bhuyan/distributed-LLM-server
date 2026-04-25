from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Literal, Optional
import hashlib
import json
from dapr.clients import DaprClient
from dapr.ext.fastapi import DaprApp

app = FastAPI()
dapp = DaprApp(app)

class Choice(BaseModel):
    text: str
    finish_reason: Optional[str] = None

# Model for full completions
class BaseLlamaResponse(BaseModel):
    id: str
    choices: List[Choice]

# Model for streaming tokens (provided in instructions)
class StreamLLamaResponse(BaseModel):
    id: str = "cmpl-7fc1be4c-8f5b-4b2f-805f-f8c5086a9fb4"
    message_idx: int = 0
    choices: List[Choice]

# CloudEvent wrappers required for Dapr FastAPI extension
class CloudEventBaseLlamaResponse(BaseModel):
    data: BaseLlamaResponse

class CloudEventStreamLlamaResponse(BaseModel):
    data: StreamLLamaResponse

class WaiterResponse(BaseModel):
    id: str = "my_cool_id"
    message_status: Literal["Starting", "Processing", "Done"] = "Starting"
    message: Optional[str] = None

def get_hash(message: str) -> str:
    return hashlib.md5(message.encode('utf8')).hexdigest()

@app.get("/api", response_model=WaiterResponse)
async def get_message_status(message: str, completion_type: Literal["completion", "streaming"]):
    msg_id = get_hash(message)
    
    with DaprClient() as client:
        # 1. Try to get existing state from Redis
        result = client.get_state("statestore", msg_id).data
        
        # 2. If result is empty, initialize the task
        if not result or len(result) == 0:
            default_state = {
                "message_status": "Starting",
                "completion_type": completion_type,
                "message": "" # Initialized as empty string or list later
            }
            # Save to Redis
            client.save_state("statestore", msg_id, json.dumps(default_state))
            
            # Send the task to the Worker via RabbitMQ
            topic = "messagestocomplete" if completion_type == "completion" else "messagestostream"
            client.publish_event(
                pubsub_name="pubsub",
                topic_name=topic,
                data=message, # The original message string
                data_content_type="text/plain"
            )
            
            return WaiterResponse(id=msg_id, message_status="Starting", message="")

        # 3. If result exists, parse and format it
        state = json.loads(result)
        current_message = state["message"]
        
        # If it's a list (streaming tokens), join them into a single string
        if isinstance(current_message, list):
            current_message = "".join(current_message)
            
        return WaiterResponse(
            id=msg_id,
            message_status=state["message_status"],
            message=current_message
        )

@dapp.subscribe(pubsub='pubsub', topic='workercompletionevents')
def handle_completion_response(message: CloudEventBaseLlamaResponse) -> None:
    with DaprClient() as client:
        data = message.data
        primary_id = data.id

        state_data = client.get_state("statestore", primary_id).data
        if not state_data:
            return
            
        current_state = json.loads(state_data)
        current_state["message"] = data.choices[0].text
        current_state["message_status"] = "Done"

        client.save_state("statestore", primary_id, json.dumps(current_state))

@dapp.subscribe(pubsub='pubsub', topic='workerstreamevents')
def add_stream_response(message: CloudEventStreamLlamaResponse) -> None:
    with DaprClient() as client:
        message = message.data
        primary_id = message.id
        interim_result = json.loads(client.get_state("statestore", primary_id).data)["message"]
        if len(interim_result) == 0:
            interim_result = [""]*(message.message_idx + 1)
            interim_result[message.message_idx] = message.choices[0].text
        else:
            if message.message_idx >= len(interim_result):
                interim_result.extend([""]*(message.message_idx + 1 - len(interim_result)))
            interim_result[message.message_idx] = message.choices[0].text
        current_state = json.loads(client.get_state("statestore", primary_id).data)
        current_state["message"] = interim_result
        current_state["message_status"] = "Processing" if message.choices[0].finish_reason is None else "Done"
        client.save_state("statestore", primary_id, json.dumps(current_state))