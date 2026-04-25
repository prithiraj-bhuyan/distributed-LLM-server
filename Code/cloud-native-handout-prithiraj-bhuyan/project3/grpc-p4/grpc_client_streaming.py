import logging
import json

import asyncio
import grpc
from llmproto.v1 import llm_pb2
from llmproto.v1 import llm_pb2_grpc

async def run() -> None:
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to get llm response ...")
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = llm_pb2_grpc.LLMServiceStub(channel)
        request = llm_pb2.LLMStreamRequest(message="What is love?")
        response_iterator = stub.LLMStream(request)
        
        print(r"\Llama Chatbot: ", end="", flush=True)
        
        async for elem in response_iterator:
            print(elem.choices[0].text, end="", flush=True)
            
        print("\n\n--- Stream Completed ---")

if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())