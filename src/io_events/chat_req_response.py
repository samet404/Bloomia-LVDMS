from uuid import uuid4

from flask_socketio import SocketIO

def chat_req_response(socketio: SocketIO):
    @socketio.on('send_chat_msg')
    def get_chat_response(json):
        id = uuid4()
        input  = json.loads(str(json))
        input = ReqChatResponse(**input)

        full_response = ""

        chat_history.append(ChatHistory(text=input.prompt, role="user"))
        chat_history.append(ChatHistory(text=full_response, role="assistant"))

