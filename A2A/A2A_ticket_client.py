from python_a2a import A2AClient

ticket_client = A2AClient("http://127.0.0.1:5010")

ticket_query = "Book a train ticket from Beijing to Shanghai."
print(f"[client] Booking ticket -> '{ticket_query}'")
ticket_result = ticket_client.ask(ticket_query)
print(f"[client] Booking result: {ticket_result}")
