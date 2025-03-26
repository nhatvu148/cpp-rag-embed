# Embedded API to Use LLM (e.g., OpenAI) in C++

This project embeds a Python-based FastAPI application within a C++ executable to leverage large language models (LLMs) like OpenAI’s GPT models. It provides a streaming chatbot API integrated into a native C++ application, with a Python client for interaction and a set of tools for managing the embedding process.

## Features
- **Embedded FastAPI Server**: Runs a FastAPI application within a C++ executable using the Python/C API.
- **Streaming Chatbot**: Provides a streaming chat endpoint powered by OpenAI’s GPT models or other large language models (LLMs).
- **Cross-Platform**: Supports macOS (ARM64) with potential for Linux and Windows compatibility.
- **Build Automation**: Uses CMake for building and Taskfile for task management.
- **Client**: Includes a Python client for testing the API.
- **Code Tools**: Scripts to combine Python files and update the C++ source with embedded code.

## Prerequisites
- **CMake**: 3.22 or higher
- **Python**: 3.13
- **C++ Compiler**: Clang++ (macOS) or equivalent
- **Homebrew** (macOS): For installing Python and dependencies
- **Task**: Task runner
- **uv**: Python package manager
- **Dependencies** (managed via `uv`):
  - `fastapi`
  - `uvicorn`
  - `openai`
  - `pydantic`
  - `python-dotenv`
  - `requests` (for the client)
  - `ruff` (for linting and formatting)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/nhatvu148/cpp-rag-embed.git
cd cpp-rag-embed
```

### 2. Set Up Python Virtual Environment with uv
```bash
# Use Python 3.13 (adjust path if needed)
brew install python@3.13

# Install uv via Homebrew (from uv docs: https://docs.astral.sh/uv/getting-started/installation/)
brew install uv

uv run sync
```

### 3. Install Task
```bash
brew install go-task/tap/go-task
```

### 4. Configure Environment
Create a .env file in the project root with your OpenAI API key:
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

## Build and Run
### Build the Project

```bash
task up
```
This cleans the build directory, generates CMake files, compiles the project, and runs the executable.
The server starts on http://0.0.0.0:23239.

### Test with the Client

```bash
task run:client
```
### Taskfile Commands

- task check-py: Lint and format Python code with Ruff.

- task clean:venv: Remove the virtual environment.

- task clean:build: Remove the build directory.

- task run:client: Run the Python client.

- task run:api: Run the FastAPI app standalone (for testing).

- task run:tools: Check Python code, combine files, and update main.cpp.

- task run:cmake: Build the project with CMake and run the executable.

- task up: Clean, build, and run the project (optionally with args, e.g., task up -- -c).

### API Endpoints
- POST /api/chat: Stream a chat response.
```bash
Request: {"message": "Hello, how are you?"}
Response: Streams text (e.g., "Hello! I'm just a program, so I don't have feelings, but I'm here and ready to help you. How can I assist you today?")
```


- GET /health: Check server status.
```bash
Response: {"status": "healthy"}
```

## License
Licensed under the [MIT License](LICENSE) (see LICENSE file).
