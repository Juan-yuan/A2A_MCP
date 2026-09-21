from python_a2a import Message, MessageRole, Task, TextContent

message = Message(content=TextContent(text="Check the weather"), role=MessageRole.USER)
task = Task(message=message.to_dict())

print(task)
print(task.to_dict())
