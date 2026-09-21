import socket
import subprocess
import sys
import time
from pathlib import Path

from mcp.server import MCPServer

HOST = "127.0.0.1"
PORT = 8001
SERVER_URL = f"http://{HOST}:{PORT}/mcp"

mcp = MCPServer("streamable_server", log_level="ERROR")


def server_is_up() -> bool:
    with socket.socket() as sock:
        sock.settimeout(0.3)
        return sock.connect_ex((HOST, PORT)) == 0


def ensure_server_running() -> None:
    if server_is_up():
        return

    subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve())],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    for _ in range(50):
        if server_is_up():
            print(f"Started MCP server at {SERVER_URL}")
            return
        time.sleep(0.1)

    raise RuntimeError(
        f"Could not connect to the MCP server at {SERVER_URL}. "
        "Run mcp_server.py first."
    )


@mcp.tool(
    name="query_high_frequency_question",
    description=(
        "Retrieve FAQs from the knowledge base and return structured "
        "JSON with questions and answers."
    ),
)
async def query_high_frequency_question() -> str:
    """Look up frequently asked questions."""
    try:
        print("FAQ tool called successfully.")
        return "Frequent question: How did the dinosaurs go extinct?"
    except Exception as e:
        print(f"Unexpected error in question retrieval: {str(e)}")
        raise


@mcp.tool(
    name="get_weather",
    description="Look up the weather",
)
async def get_weather() -> str:
    """Weather lookup tool."""
    try:
        print("Weather tool called.")
        return "Beijing is cloudy."
    except Exception as e:
        print(f"Unexpected error in question retrieval: {str(e)}")
        raise


if __name__ == "__main__":
    print("Starting the MCP streamable-http server...")
    print(f"HTTP endpoint: {SERVER_URL}")
    print("Press Ctrl+C to stop the server")

    try:
        mcp.run(transport="streamable-http", host=HOST, port=PORT)
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Failed to start the server: {e}")
