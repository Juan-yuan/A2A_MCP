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
    description="A ticket booking agent.",
    url=f"http://{HOST}:{PORT}",
    version="1.0.0",
    skills=[
        AgentSkill(
            name="book_ticket",
            description="Book a ticket from the user request.",
            tags=["ticket", "booking"],
            examples=["Book a train ticket from Beijing to Shanghai tomorrow."],
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
    def book_ticket(self, request_text: str) -> str:
        if not request_text.strip():
            return "Please tell me what ticket you want to book."
        return f"Booked. I received your request: {request_text.strip()}"

    def handle_task(self, task):
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else str(content or "")

        print(f"Task state: {task.status.state}")
        print(f"Request: {text}")

        response_text = self.book_ticket(text)
        task.artifacts = [{"parts": [{"type": "text", "text": response_text}]}]
        task.status = TaskStatus(state=TaskState.COMPLETED)
        return task


if __name__ == "__main__":
    server = TicketServer()
    print(f"[{server.agent_card.name}] server created")
    print(f"Listening on http://{HOST}:{PORT}")
    run_server(server, host=HOST, port=PORT, debug=False)
