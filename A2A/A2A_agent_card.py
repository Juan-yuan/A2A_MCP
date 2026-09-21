from python_a2a import AgentCard, AgentSkill

ticket_skill = AgentSkill(
    name="book_ticket",
    description="Book a train ticket.",
    examples=["Book a train ticket from Shanghai to Beijing."],
    input_modes=["text/plain"],
    output_modes=["text/plain"],
)

agent_card = AgentCard(
    name="TicketAgent",
    description="An agent that can book tickets.",
    url="http://127.0.0.1:5009",
    version="1.0.0",
    skills=[ticket_skill],
    capabilities={"streaming": True},
)

print(agent_card)
print(agent_card.to_dict())
