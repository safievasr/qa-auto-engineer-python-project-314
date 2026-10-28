import uuid


def make_user(prefix: str = "auto") -> dict:
    uid = uuid.uuid4().hex[:8]
    return {
        "email": f"{prefix}_{uid}@example.com",
        "first_name": f"First{uid}",
        "last_name": f"Last{uid}",
    }


INVALID_EMAILS = [
    "user@",
    "@example.com",
]