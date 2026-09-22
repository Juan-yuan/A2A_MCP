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
PORT = 5008

agent_card = AgentCard(
    name="WeatherAgentServer",
    description="A weather lookup expert agent.",
    url=f"http://{HOST}:{PORT}",
    version="1.0.0",
    skills=[
        AgentSkill(
            name="query_weather",
            description="Look up the weather for a city.",
            tags=["weather"],
            examples=["What is the weather in Beijing?"],
        )
    ],
)


class WeatherAgentServer(A2AServer):
    def __init__(self):
        super().__init__(agent_card=agent_card)

    @skill(
        name="query_weather",
        description="Look up the weather for a city.",
        tags=["weather"],
    )
    def query_weather(self, query: str) -> str:
        query_lower = query.lower()
        if "shanghai" in query_lower:
            return "Shanghai is cloudy, 24°C."
        return "Beijing is sunny, 30°C."

    def handle_task(self, task):
        message_data = task.message or {}
        content = message_data.get("content", {})
        query = content.get("text", "") if isinstance(content, dict) else str(content or "")

        print(f"[{self.agent_card.name}] received task: {query}")

        if "weather" in query.lower():
            weather_result = self.query_weather(query)
            print(f"[{self.agent_card.name}] weather result: {weather_result}")
            task.artifacts = [{"parts": [{"type": "text", "text": weather_result}]}]
        else:
            task.artifacts = [{"parts": [{"type": "text", "text": "I can look up the weather. Ask about a city."}]}]

        task.status = TaskStatus(state=TaskState.COMPLETED)
        print(f"[{self.agent_card.name}] task completed")
        return task


if __name__ == "__main__":
    server = WeatherAgentServer()
    print(f"[{server.agent_card.name}] listening on {server.agent_card.url}")
    run_server(server, host=HOST, port=PORT, debug=False)
