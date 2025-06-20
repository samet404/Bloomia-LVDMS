# ==============================================================================
# This file defines constants that are used in socketio events
# ==============================================================================

def RECEIVE_CHAT_MSG_FROM_POOL_EVENT(session_id: str):
    return f"receive_chat_msg:{session_id}"
