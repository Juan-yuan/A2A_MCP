import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcp import Client
from mcp_server import mcp


async def main() -> None:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        print("tools-->", [tool.name for tool in tools.tools])

        weather = await client.call_tool("get_weather")
        print("result-->", weather)

        faq = await client.call_tool("query_high_frequency_question")
        print("result2-->", faq)


if __name__ == "__main__":
    asyncio.run(main())
