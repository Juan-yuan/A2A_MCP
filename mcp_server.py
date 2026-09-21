from mcp.server import MCPServer

mcp = MCPServer("streamable_server", log_level="ERROR")


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
    print("HTTP endpoint: http://127.0.0.1:8001/mcp")
    print("Press Ctrl+C to stop the server")

    try:
        mcp.run(transport="streamable-http", host="127.0.0.1", port=8001)
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Failed to start the server: {e}")
