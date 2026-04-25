"""FastAPI server for LLM inference using TinyLlama."""

from llama_cpp import Llama
from fastapi import FastAPI, Query, Depends
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator
from typing import List, Any
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

LLM_MODEL: Llama | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # pragma: no cover
    """Add LLM_MODEL to app context at startup."""
    global LLM_MODEL
    LLM_MODEL = Llama(
        model_path="tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
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


class Usage(BaseModel):
    """Usage statistics for the LLM completion."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Choices(BaseModel):
    """Completion choices returned by the LLM."""

    text: str = "Beep boop"
    index: int = 0
    logprobs: str | None = None
    finish_reason: str = "stop"


class BaseLlamaResponse(BaseModel):
    """The full response object for the LLM API."""

    id: str = "cmpl-7fc1be4c-8f5b-4b2f-805f-f8c5086a9fb4"
    object: str = "text_completion"
    created: int = 1708459650
    model: str = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
    usage: Usage
    choices: List[Choices]


# TODO: Implement the healthcheck api route here
@app.get("/healthcheck")
async def healthcheck() -> str:
    """Returns a simple health status string.

    Returns:
        str: A string indicating the health status of the API.
    """
    return "OK"


# TODO: Implement the LLM api route here
@app.get("/api", response_model=BaseLlamaResponse)
async def llm_api(prompt_data: LLMPrompt = Depends(LLMPrompt)) -> Any:
    """Handles LLM inference requests asynchronously.

    Args:
        prompt_data (LLMPrompt): The user message to process.

    Returns:
        Any: A response object containing the LLM completion.
    """
    prompt = f"User: {prompt_data.message}\nAssistant:"

    return await asyncio.to_thread(get_llm(), prompt, temperature=0.0, max_tokens=None)
