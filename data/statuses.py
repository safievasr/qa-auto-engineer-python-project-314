import uuid


def make_status(prefix: str = "auto") -> dict:
    uid = uuid.uuid4().hex[:8]
    return {
        "name": f"{prefix} {uid}",
        "slug": f"{prefix}-{uid}",
    }