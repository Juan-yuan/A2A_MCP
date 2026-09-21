import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import StructuredTool
from mcp import Client

from mcp_server import mcp

model = init_chat_model(
    model="qwen2.5:7b",
    model_provider="ollama",
    base_url="http://localhost:11434/",
    temperature=0.1,
    reasoning=False,
)


def text_from_tool_result(result) -> str:
    texts = [
        block.text
        for block in (result.content or [])
        if getattr(block, "text", None)
    ]
    return "\n".join(texts) or str(result)


def wrap_mcp_tools(client: Client, mcp_tools) -> list[StructuredTool]:
    langchain_tools = []
    for mcp_tool in mcp_tools:
        tool_name = mcp_tool.name
        tool_description = mcp_tool.description or mcp_tool.name

        async def _arun(*, _name=tool_name) -> str:
            result = await client.call_tool(_name)
            return text_from_tool_result(result)

        _arun.__name__ = tool_name
        _arun.__doc__ = tool_description
        langchain_tools.append(
            StructuredTool.from_function(
                name=tool_name,
                description=tool_description,
                coroutine=_arun,
            )
        )
    return langchain_tools


async def main() -> None:
    async with Client(mcp) as client:
        listed = await client.list_tools()
        tools = wrap_mcp_tools(client, listed.tools)
        print("tools-->", [tool.name for tool in tools])

        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=(
                "You are a helpful assistant that can call tools to answer questions."
            ),
        )

        print("MCP client started. Type 'quit' to exit.")
        while True:
            query = input("\nQuery: ").strip()
            if query.lower() == "quit":
                break
            try:
                result = await agent.ainvoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": query,
                            }
                        ]
                    }
                )
                print(result["messages"][-1].content)
            except Exception as e:
                print(f"Failed to parse the response: {e}")


if __name__ == "__main__":
    asyncio.run(main())
