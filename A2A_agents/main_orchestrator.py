import asyncio
import json
import uuid

from python_a2a import AgentNetwork, Message, MessageRole, Task, TextContent


async def main():
    network = AgentNetwork(name="TravelOrchestrator")
    network.add("TicketAgent", "http://127.0.0.1:5009")
    network.add("WeatherAgent", "http://127.0.0.1:5008")
    print("[orchestrator] AgentNetwork ready. Registered agents:")
    for agent_info in network.list_agents():
        print(json.dumps(agent_info, indent=4, ensure_ascii=False))
    print("-" * 50)

    weather_query = "What is the weather in Beijing?"
    weather_client = network.get_agent("WeatherAgent")

    weather_ask_result = weather_client.ask(weather_query)
    print("[orchestrator] Weather ask() result:")
    print(weather_ask_result)

    weather_message = Message(content=TextContent(text=weather_query), role=MessageRole.USER)
    weather_task = Task(message=weather_message.to_dict(), id="task-" + str(uuid.uuid4()))
    weather_result = await weather_client.send_task_async(weather_task)

    weather_info = "unknown weather"
    try:
        weather_parts = weather_result.artifacts[0]["parts"]
        if weather_parts and weather_parts[0].get("type") == "text":
            weather_info = weather_parts[0].get("text")
            print(f"[orchestrator] WeatherAgent task result: '{weather_info}'")
    except Exception as e:
        print(f"[orchestrator] Failed to parse weather result: {e}")

    ticket_query = (
        f"Book a train ticket from Beijing to Shanghai. Current weather: {weather_info}"
    )
    ticket_client = network.get_agent("TicketAgent")
    ticket_message = Message(content=TextContent(text=ticket_query), role=MessageRole.USER)
    ticket_task = Task(message=ticket_message.to_dict(), id="task-" + str(uuid.uuid4()))
    ticket_result = await ticket_client.send_task_async(ticket_task)

    print("\n[orchestrator] TicketAgent final result:")
    print(json.dumps(ticket_result.to_dict(), indent=4, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
