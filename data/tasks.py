import uuid


def make_task(
    prefix: str = "auto",
    status: str = "Draft",
    assignee: str = "jane@gmail.com",
    content: str | None = None,
    labels: list[str] | None = None,
) -> dict:
    uid = uuid.uuid4().hex[:8]
    result = {
        "title": f"{prefix}-{uid}",
        "status": status,
        "assignee": assignee,
    }
    if content is not None:
        result["content"] = content
    if labels:
        result["labels"] = labels
    return result