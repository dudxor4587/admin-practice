import uuid
from typing import Any

from fastapi import HTTPException, Request

sessions = {}


def create_session(user_id: int) -> str:
    session_id = str(uuid.uuid4())
    sessions[session_id] = user_id
    return session_id


def get_user_id_from_session(request: Request) -> Any | None:
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        return sessions[session_id]
    return None


def delete_session(request: Request) -> None:
    session_id = request.cookies.get("session_id")
    if session_id in sessions:
        del sessions[session_id]
    else:
        raise HTTPException(status_code=404, detail="Session not found")
