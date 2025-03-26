from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
import uvicorn
from dotenv import load_dotenv
from typing import List, Dict, Generator
from collections import deque
from openai import OpenAI, OpenAIError

load_dotenv()


class Config:
    TITLE = "Chatbot API"
    SYSTEM_MESSAGE = "You are a helpful assistant."
    MODEL = "gpt-4o-mini"
    HISTORY_MAXLEN = 20
    HOST = "0.0.0.0"
    PORT = 23239


app = FastAPI(title=Config.TITLE)

conversation_history = deque(maxlen=Config.HISTORY_MAXLEN)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class MessageRequest(BaseModel):
    message: str


def generate_chat_stream(message: str) -> Generator[str, None, None]:
    """Generate streaming chat response from OpenAI."""
    try:
        messages = [
            {"role": "system", "content": Config.SYSTEM_MESSAGE},
            {"role": "user", "content": message},
        ]

        stream = client.chat.completions.create(
            model=Config.MODEL, messages=messages, stream=True
        )

        full_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content is not None:
                full_response += content
                yield content

        conversation_history.append({"role": "user", "content": message})
        conversation_history.append({"role": "assistant", "content": full_response})

    except OpenAIError as e:
        yield f"OPENAI_ERROR: {str(e)}\n\n"
    except Exception as e:
        yield f"ERROR: {str(e)}\n\n"
    finally:
        if "stream" in locals():
            stream.close()


@app.post("/api/chat")
def chat_stream_endpoint(request: MessageRequest) -> StreamingResponse:
    """Handle chat streaming endpoint."""
    return StreamingResponse(
        generate_chat_stream(request.message), media_type="text/event-stream"
    )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


def main():
    """Run the FastAPI application."""
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)


if __name__ == "__main__":
    main()
