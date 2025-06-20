from flask_socketio import SocketIO

from src.ai_pool import ai_pool
from src.io_events_constants import RECEIVE_CHAT_MSG_FROM_POOL_EVENT

def pool_on_chat_msg(socketio: SocketIO, session_id: str):
    @ai_pool.on(f'{RECEIVE_CHAT_MSG_FROM_POOL_EVENT}:{session_id}')
    def on_chat_msg(data):
        print(data)