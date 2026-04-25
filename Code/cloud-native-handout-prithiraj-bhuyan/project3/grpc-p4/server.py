"""The Python implementation of the GRPC LLM.Completion server."""

import logging
import time
import asyncio
from typing import Any, AsyncGenerator

import grpc
from llmproto.v1 import llm_pb2
from llmproto.v1 import llm_pb2_grpc
from llama_cpp import Llama
from google.protobuf.timestamp_pb2 import Timestamp

MODEL_PATH = "../../llm_server/tinyllama-1.1b-chat-v1.0.Q2_K.gguf"

class LLMService(llm_pb2_grpc.LLMServiceServicer):
    def __init__(self, model: Any) -> None:
        """Initialize with the pre-loaded Llama model."""
        self.model = model

    async def Completion(self, request: llm_pb2.CompletionRequest, context: grpc.ServicerContext) -> llm_pb2.CompletionResponse:
        """
        Handles the Completion RPC request.
        Translates the request message into an LLM response object.
        """
        print(f"Received message: {request.message}")

        #Token validation (as per Task 1 logic)
        tokens = self.model.tokenize(request.message.encode("utf-8"))
        if len(tokens) > 512:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Token count exceeds 512 limit.")
        
        prompt = f"User: {request.message}\nAssistant:"
        raw_response = self.model(
            prompt,
            temperature=0.0,
            max_tokens=None,
            stop=["User:", "\nUser:"]
        )

        created_at = Timestamp()
        created_at.FromSeconds(int(raw_response["created"]))

        return llm_pb2.CompletionResponse(
            id=raw_response["id"],
            object=raw_response["object"],
            created=created_at,
            model=raw_response["model"],
            usage=llm_pb2.Usage(
                prompt_tokens=raw_response["usage"]["prompt_tokens"],
                completion_tokens=raw_response["usage"]["completion_tokens"],
                total_tokens=raw_response["usage"]["total_tokens"]
            ),
            choices=[
                llm_pb2.Choice(
                    text=c["text"],
                    index=c["index"],
                    logprobs=str(c.get("logprobs") or ""),
                    finish_reason=c["finish_reason"]
                ) for c in raw_response["choices"]
            ]
        )

    async def LLMStream(self, request: llm_pb2.LLMStreamRequest, context: grpc.ServicerContext) -> AsyncGenerator[llm_pb2.LLMStreamResponse, None]:
        """
        Streaming response logic using a generator function.
        Yields chunks of text as the LLM generates them.
        """
        print(f"Starting stream for: {request.message}")
        prompt = f"<|user|>\n{request.message}</s>\n<|assistant|>\n"
        
        # We enable stream=True to get an iterator from llama-cpp
        stream_iterator = self.model(
            prompt,
            temperature=0.0,
            max_tokens=256,
            stop=["</s>", "<|user|>", "User:"],
            stream=True 
        )

        for chunk in stream_iterator:
            # 1. Create the Timestamp for this specific chunk
            created_at = Timestamp()
            created_at.FromSeconds(int(chunk["created"]))
            
            # 2. Extract data from the first choice in the chunk
            choice_data = chunk["choices"][0]
            
            # 3. Yield a StreamingResponse object (omitting the usage field as requested)
            yield llm_pb2.LLMStreamResponse(
                id=chunk["id"],
                object=chunk["object"],
                created=created_at,
                model=chunk["model"],
                choices=[
                    llm_pb2.Choice(
                        text=choice_data.get("text", ""),
                        index=choice_data.get("index", 0),
                        logprobs=str(choice_data.get("logprobs") or ""),
                        finish_reason=choice_data.get("finish_reason") or ""
                    )
                ]
            )


async def serve() -> None:
    # Instantiate the model inside the main thread to prevent double loading
    print(f"Loading model from {MODEL_PATH}...")
    try:
        llm_model = Llama(
            model_path=MODEL_PATH,
            n_ctx=512,
            n_batch=1,
        )
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    # Initialize the gRPC server
    server = grpc.aio.server()
    llm_pb2_grpc.add_LLMServiceServicer_to_server(LLMService(llm_model), server)
    
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    await server.start()
    print(f"gRPC Server successfully started on port {port}")
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())