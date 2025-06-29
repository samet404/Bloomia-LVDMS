import logging

from flask_socketio import SocketIO
import uuid
from src.ai_pool import ai_pool, AIPoolStreamReqInput
from src.data_classes import SendMessageInput

# This function is responsible for sending, receiving and handling chat messages
# This function uses the AI Pool to generate responses
def send_chat_msg(socketio: SocketIO, session_id: str):
    # We are using unique IDs on each request to prevent duplicate responses at the same time
    ids = set()

    @socketio.on('send-chat-msg')
    def send_chat_msg(json):
        full_response = ""

        try:
            input = json.loads(str(json))
            input = SendMessageInput(**input)

            id = uuid.uuid4()
            while id in ids:
                id = uuid.uuid4()

            @ai_pool.on(f"receive-chat-msg:session:{session_id}:ID:{id}")
            def on_chat_msg(data):
                socketio.emit(f"receive-chat-msg", data)

            @ai_pool.on(f"receive-chat-msg:session:{session_id}:ID:{id}:error")
            def on_chat_msg_error(data):
                print("Error in AI Pool: ", data)

            @ai_pool.on(f"receive-chat-msg:session:{session_id}:ID:{id}:success")
            def on_chat_msg_success(data):
                print("Success in AI Pool: ", data)

            ai_pool.emit("stream-req", AIPoolStreamReqInput(
                prompt=input.prompt,
                model=,
                sio_event=f"receive-chat-msg:session:{session_id}:ID:{id}",
                metadata=None
            ), namespace = '/')
        except Exception as e:
            logging.error(f"Error in send_chat_msg: {str(e)}")