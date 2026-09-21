from python_a2a import AIAgentRouter, AgentNetwork, OllamaA2AClient

network = AgentNetwork(name="MyNetwork")
network.add("TicketAgent", "http://127.0.0.1:5010")

llm = OllamaA2AClient(
    api_url="http://localhost:11434",
    model="qwen2.5:7b",
    temperature=0.1,
)

router = AIAgentRouter(llm_client=llm, agent_network=network)
question = "Book a train ticket from Beijing to Shanghai."
agent_name, confidence = router.route_query(question)
print(f"{agent_name} (confidence={confidence})")

client = network.get_agent(name=agent_name)
print(client.ask(question))
