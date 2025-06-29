import logging
from flask_socketio import SocketIO
from src.ai_pool import ai_pool
from src.stores.opened_aipool_events_store import OpenedAIPoolEventsStore


def on_disconnect(socketio: SocketIO, session_id: str, auth_session_id: str, opened_aipool_events: OpenedAIPoolEventsStore):
    @socketio.on('disconnect')
    def handle_disconnect():
        logging.info(f'USER DISCONNECTED FROM WEBSOCKET SERVER \n session_id: {session_id} | auth_session_id: {auth_session_id}')

        # Remove events from AI pool socketio handdddlers
        for event_name in opened_aipool_events.events:
            ai_pool.handlers['/'].pop(event_name)
