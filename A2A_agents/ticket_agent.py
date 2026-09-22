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
PORT = 5009

ticket_card = AgentCard(
    name="TicketAgentServer",
    description="A ticket booking expert agent.",
    url=f"http://{HOST}:{PORT}",
    version="1.0.0",
    skills=[
        AgentSkill(
            name="book_ticket",
            description="Book a ticket from the user request.",
            tags=["ticket", "booking"],
            examples=["Book a train ticket from Beijing to Shanghai."],
        )
    ],
)


class TicketServer(A2AServer):
    def __init__(self):
        super().__init__(agent_card=ticket_card)

    @skill(
        name="book_ticket",
        description="Book a ticket from the user request.",
        tags=["ticket", "booking"],
    )
    def book_ticket(self, query: str) -> str:
        query_lower = query.lower()
        if "shanghai" in query_lower and "beijing" in query_lower:
            return "Booked a train ticket from Beijing to Shanghai. Train G1001, car 10, seat 1A."
        if not query.strip():
            return "Please tell me what ticket you want to book."
        return "Please specify both the departure city and the destination."

    def handle_task(self, task):
        message_data = task.message or {}
        content = message_data.get("content", {})
        query = content.get("text", "") if isinstance(content, dict) else str(content or "")

        print(f"[{self.agent_card.name}] received task: {query}")
        train_result = self.book_ticket(query)
        print(f"[{self.agent_card.name}] result: {train_result}")

        task.artifacts = [{"parts": [{"type": "text", "text": train_result}]}]
        task.status = TaskStatus(state=TaskState.COMPLETED)
        print(f"[{self.agent_card.name}] task completed")
        return task


if __name__ == "__main__":
    server = TicketServer()
    print(f"[{server.agent_card.name}] listening on {server.agent_card.url}")
    run_server(server, host=HOST, port=PORT, debug=False)
