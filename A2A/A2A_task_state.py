from python_a2a import TaskState

if TaskState.COMPLETED == "completed":
    print("Task completed")

state = TaskState.SUBMITTED
print("State value:", state.value)
print(state)
