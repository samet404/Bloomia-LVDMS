from flask_socketio import SocketIO, emit
from pymilvus import MilvusClient

def ws(socketio: SocketIO, milvus: MilvusClient):
    @socketio.on('connect', namespace='/ws')
    def handle_connect():
        print('connected')
        emit('my response', {'data': 'got it!'}, namespace='/ws')