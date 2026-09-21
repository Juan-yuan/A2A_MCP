from python_a2a import A2AClient

AGENT_URL = "http://127.0.0.1:8005"

client = A2AClient(AGENT_URL)
query = "What is the weather in Beijing?"
print(f"[client] Sending to {AGENT_URL}: {query}")
result = client.ask(query)
print(f"[client] Result: {result}")
