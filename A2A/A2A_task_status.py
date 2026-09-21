from python_a2a import TaskState, TaskStatus

status_completed = TaskStatus(
    state=TaskState.COMPLETED,
    message={"info": "Task completed successfully"},
)

status_failed = TaskStatus(
    state=TaskState.FAILED,
    message={"error": "Unable to process the request"},
)

print("Completed status:", status_completed.to_dict())
print("Failed status:", status_failed.to_dict())
