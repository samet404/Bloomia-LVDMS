from flask_socketio import SocketIO

def send_io_client_error(socketio: SocketIO, error: str, to: str):
    socketio.emit('error', error, to=to)