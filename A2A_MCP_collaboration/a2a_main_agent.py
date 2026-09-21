import httpx
from python_a2a import (
    A2AServer,
    AgentCard,
    AgentSkill,
    TaskState,
    TaskStatus,
    run_server,
    skill,
)

HOST = "127.0.0.1"
PORT = 8005
MCP_URL = "http://127.0.0.1:6005"

agent_card = AgentCard(
    name="WeatherServer",
    description="An A2A agent that looks up weather through an MCP tool.",
    url=f"http://{HOST}:{PORT}",
    version="1.0.0",
    skills=[
        AgentSkill(
            name="get_weather",
            description="Look up the weather for a city.",
            tags=["weather"],
            examples=["What is the weather in Beijing?"],
        )
    ],
)


class WeatherServer(A2AServer):
    def __init__(self):
        super().__init__(agent_card=agent_card)

    @skill(
        name="get_weather",
        description="Look up the weather for a city.",
        tags=["weather"],
    )
    def get_weather(self, city: str) -> str:
        response = httpx.post(
            f"{MCP_URL}/tools/get_weather",
            json={"city": city},
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()
        content = data.get("content") or []
        if content and isinstance(content[0], dict):
            return content[0].get("text") or str(data)
        return str(data)

    def _city_from_query(self, query: str) -> str:
        query_lower = query.lower()
        for city in ("beijing", "shanghai"):
            if city in query_lower:
                return city.title()
        return "Beijing"

    def handle_task(self, task):
        message_data = task.message or {}
        content = message_data.get("content", {})
        query = content.get("text", "") if isinstance(content, dict) else str(content or "")

        print(f"Task state: {task.status.state}")
        print(f"Request: {query}")

        if "weather" in query.lower():
            city = self._city_from_query(query)
            try:
                result_text = self.get_weather(city)
            except Exception as exc:
                result_text = f"Weather lookup failed: {exc}"
        else:
            result_text = "I can look up the weather. Ask about a city."

        task.artifacts = [{"parts": [{"type": "text", "text": result_text}]}]
        task.status = TaskStatus(state=TaskState.COMPLETED)
        print(f"[{self.agent_card.name}] result: {result_text}")
        return task


if __name__ == "__main__":
    server = WeatherServer()
    print(f"[{server.agent_card.name}] server created")
    print(f"Listening on http://{HOST}:{PORT}")
    print(f"MCP weather tool: {MCP_URL}")
    run_server(server, host=HOST, port=PORT, debug=False)
