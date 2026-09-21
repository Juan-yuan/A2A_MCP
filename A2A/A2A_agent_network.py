from python_a2a import AgentNetwork

network = AgentNetwork(name="MyNetwork")
network.add(name="TicketAgent", agent_or_url="http://127.0.0.1:5010")

print(f"network agents --> {network.agent_cards}")

client = network.get_agent(name="TicketAgent")
print(client.ask("Book a train ticket from Beijing to Shanghai."))
