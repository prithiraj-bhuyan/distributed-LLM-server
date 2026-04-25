"""FastAPI server for LLM inference using TinyLlama."""

from llama_cpp import Llama
from fastapi import FastAPI, Query, Depends
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator
from typing import List, Any, Literal, AsyncGenerator
import asyncio
from contextlib import asynccontextmanager
from dapr.ext.fastapi import DaprApp
import hashlib
from dapr.clients import DaprClient
import json

LLM_MODEL: Llama | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # pragma: no cover
    """Add LLM_MODEL to app context at startup."""
    global LLM_MODEL
    LLM_MODEL = Llama(
        model_path="../../../llm_server/tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
        n_ctx=512,
        n_batch=1,
    )
    yield
    del LLM_MODEL


def get_llm() -> Llama:
    """Get LLM_MODEL or raise an assertion error."""
    assert LLM_MODEL is not None
    return LLM_MODEL


app = FastAPI(lifespan=lifespan)
dapr = DaprApp(app)

class LLMPrompt(BaseModel):
    """Data model for user prompts."""

    message: str = Query(..., description="User message")

    @field_validator("message")
    @classmethod
    def check_token_count(cls, v: str) -> str:
        """Validates that the message does not exceed the token limit.

        Args:
            v (str): The user message to validate.

        Returns:
            str: The validated user message.

        Raises:
            RequestValidationError: If the token count exceeds the limit.
        """
        tokens = get_llm().tokenize(v.encode("utf-8"))
        if len(tokens) > 512:
            error_msg = "Token count exceeds the maximum allowed limit of 512."
            raise RequestValidationError(error_msg)
        return v

class SimpleCloudEvent(BaseModel):
    """Generic CloudEvent structure for Dapr."""
    data: str

def get_hash(message:str) -> str:
    return hashlib.md5(message.encode('utf8')).hexdigest()

# TODO: Implement the healthcheck api route here
@app.get("/healthcheck")
async def healthcheck() -> str:
    """Returns a simple health status string.

    Returns:
        str: A string indicating the health status of the API.
    """
    return "OK"


# TODO: Implement the LLM api route here

@dapr.subscribe(pubsub="pubsub", topic="messagestocomplete")
async def handle_complete(event: SimpleCloudEvent) -> Literal["OK"]:
    try:
        prompt_data = LLMPrompt(message=event.data)
        template = f"User: {prompt_data.message}\nAssistant:"
        response = await asyncio.to_thread(get_llm(), template, temperature=0.0, max_tokens=None)

        hashed_id = get_hash(prompt_data.message)
        response["id"] = hashed_id
        
        print(response)
        with DaprClient() as client:
            client.publish_event(pubsub_name="pubsub", topic_name="workercompletionevents", data=json.dumps(response), data_content_type="application/json")
        print("Published to Master Service")
        
    except Exception as e:
        print(f"Error in completion: {e}")
    
    return "OK"

@dapr.subscribe(pubsub="pubsub", topic="messagestostream")
async def handle_stream(event: SimpleCloudEvent) -> Literal["OK"]:
    try:
        prompt_data = LLMPrompt(message=event.data)
        template = f"User: {prompt_data.message}\nAssistant:"
        llm = get_llm()
        hashed_id = get_hash(prompt_data.message)
        
        with DaprClient() as client:
            for idx, elem in enumerate(llm(template, temperature=0.0, stream=True, max_tokens=None)):
                elem["id"] = hashed_id
                elem["message_idx"] = idx
                
                print(elem, end="", flush=True)
                client.publish_event(pubsub_name="pubsub", topic_name="workerstreamevents", data=json.dumps(elem), data_content_type="application/json")
                print("\nPublished to Master Service")
    except Exception as e:
        print(f"Error in stream: {e}")
    
    return "OK"