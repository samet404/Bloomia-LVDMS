from uuid import uuid4

from flask_socketio import SocketIO

from src.data_classes import SendMessageInput
from src.io_events_constants import RECEIVE_CHAT_MSG_FROM_POOL_EVENT


def send_chat_msg(socketio: SocketIO, session_id: str):
    @socketio.on
    def send_chat_msg(json):
        input = json.loads(str(json))
        input = SendMessageInput(**input)

        socketio.emit(RECEIVE_CHAT_MSG_FROM_POOL_EVENT(session_id), input.prompt, namespace='/')
