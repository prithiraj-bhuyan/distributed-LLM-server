# just a sample for testing pubsub subscription

from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from typing import Literal

app = FastAPI()
dapp = DaprApp(app)

class SimpleCloudEvent(BaseModel):
    data: str
    datacontenttype: str
    id: str
    pubsubname: str
    source: str
    specversion: str
    topic: str
    traceid: str
    traceparent: str
    tracestate: str
    type: str  

@dapp.subscribe(pubsub="pubsub", topic="workermessages")
def print_test_message(message: SimpleCloudEvent) -> Literal["OK"]:
    print(message.data)
    return "OK"