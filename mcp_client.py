import asyncio

from mcp import Client

SERVER_URL = "http://127.0.0.1:8001/mcp"


async def main() -> None:
    async with Client(SERVER_URL) as client:
        tools = await client.list_tools()
        print("tools-->", [tool.name for tool in tools.tools])

        weather = await client.call_tool("get_weather")
        print("result-->", weather)

        faq = await client.call_tool("query_high_frequency_question")
        print("result2-->", faq)


if __name__ == "__main__":
    asyncio.run(main())
