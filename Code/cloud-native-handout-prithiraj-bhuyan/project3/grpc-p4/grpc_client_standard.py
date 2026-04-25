import logging
import json

import asyncio
import grpc
from llmproto.v1 import llm_pb2
from llmproto.v1 import llm_pb2_grpc
from google.protobuf.json_format import MessageToDict


async def run() -> None:
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to get llm response ...")
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = llm_pb2_grpc.LLMServiceStub(channel)
        response = await stub.Completion(llm_pb2.CompletionRequest(message="what is love?"))
        response_dict = MessageToDict(
            response, 
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True
        )
    print("\n--- Full Response ---")
    print(json.dumps(response_dict, indent=4))


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())