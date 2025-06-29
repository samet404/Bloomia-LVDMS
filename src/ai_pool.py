import logging
from typing import Literal

import socketio
from pydantic import BaseModel

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


class AIPoolStreamReqInput(BaseModel):
    prompt: str
    model: Literal[
        'gemma-3-1b-it', 'gemma-3-27b-it', 'gemma-3-4b-it', 'gemma-3-12b-it', 'gemma-3n-e4b-it', 'gemini-2.0-flash', 'gemini-2.0-flash-lite', 'gemini-2.5-pro-preview-06-05', 'gemini-1.5-pro']
    sio_event: str
    metadata: str | None = None
