"""API Server Tests."""

from fastapi.testclient import TestClient
from llm_server.main import app, LLMPrompt
from fastapi.exceptions import RequestValidationError
from unittest.mock import patch

client = TestClient(app=app)


def test_health_route() -> None:
    """Test for health endpoint."""
    response = client.get("/healthcheck")
    assert response.status_code == 200


def test_api() -> None:
    """Test for LLM apis."""
    with patch("llm_server.main.LLM_MODEL") as llm:
        llm.return_value = {
            "id": "cmpl-f1737a06-56fb-47b5-a989-722b9d86f50e",
            "object": "text_completion",
            "created": 1713560037,
            "model": "tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
            "choices": [
                {
                    "text": "\n     Hey there! I hope you're having a great day so far. How about we chat about the latest news and updates in the tech industry? I'm always up-to-date on the latest trends, so let's get right to it. Firstly, what are some of the most exciting developments in the tech world that you think we should all be keeping an eye on? Secondly, can you tell me about any new innovations or advancements in the field of AI and how they might impact our daily lives? I'm always up for a good chat about",
                    "index": 0,
                    "logprobs": "",
                    "finish_reason": "length",
                }
            ],
            "usage": {
                "prompt_tokens": 37,
                "completion_tokens": 128,
                "total_tokens": 165,
            },
        }

        response = client.get("/api?message=hello")
        assert response.status_code == 200


def test_token_count_happy_path() -> None:
    """Test for count happy path."""
    with patch("llm_server.main.LLM_MODEL") as llm:
        llm.tokenize.return_value = [1]
        assert isinstance(LLMPrompt(message="This is a test"), LLMPrompt)

        try:
            llm.tokenize.return_value = [1] * 1000
            LLMPrompt(message="bad_message")
        except RequestValidationError as e:
            actual_error_msg = "".join(e.errors())

            expected = "Token count exceeds the maximum allowed limit of 512."
            assert actual_error_msg == expected
