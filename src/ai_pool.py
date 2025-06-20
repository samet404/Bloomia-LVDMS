import logging

import socketio

logging.info('Connecting to AI Pool...')
ai_pool = socketio.Client()

@ai_pool.on('connect')
def on_connect():
    print('Connected to AI Pool')

@ai_pool.on('disconnect')
def on_disconnect():
    print('Disconnected from AI Pool')
    logging.error('Disconnected from AI Pool')
    raise Exception('Disconnected from AI Pool')
