import requests
from typing import Optional
import sys


class ChatClient:
    """A client for streaming chat responses from a FastAPI server."""

    def __init__(self, base_url: str = "http://localhost:23239"):
        """Initialize the client with a base URL."""
        self.base_url = base_url
        self.headers = {
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        }
        self.chunk_size = 1  # Bytes per chunk

    def stream(self, message: str) -> None:
        """Stream a chat response from the server."""
        url = f"{self.base_url}/api/chat"
        payload = {"message": message}

        try:
            with requests.post(
                url, json=payload, headers=self.headers, stream=True
            ) as response:
                response.raise_for_status()
                for chunk in response.iter_content(
                    chunk_size=self.chunk_size, decode_unicode=True
                ):
                    if chunk:
                        if chunk.strip().startswith("ERROR: "):
                            print(
                                f"\nError from server: {chunk[7:].strip()}",
                                file=sys.stderr,
                            )
                            return
                        print(chunk, end="", flush=True)
        except requests.RequestException as e:
            print(f"\nNetwork error: {str(e)}", file=sys.stderr)


def main():
    """Run the chat client in an interactive loop."""
    client = ChatClient()
    print("Enter your message (type 'exit' to stop):")

    while True:
        message = input("\n> ").strip()
        if message.lower() == "exit":
            print("Exiting...")
            break
        if message:
            client.stream(message)


if __name__ == "__main__":
    main()
