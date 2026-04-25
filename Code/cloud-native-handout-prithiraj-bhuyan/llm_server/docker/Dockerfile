FROM python:3.12-alpine

WORKDIR /app

RUN apk update && apk add gcc libc-dev g++ cmake make linux-headers

COPY dist/llm_server-0.1.0-py3-none-any.whl /app/
COPY tinyllama-1.1b-chat-v1.0.Q2_K.gguf /app/

RUN pip install llm_server-0.1.0-py3-none-any.whl

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "llm_server.main:app", "--host", "0.0.0.0", "--port", "8000"]