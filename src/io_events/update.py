import logging
from flask import session, request
from flask_socketio import SocketIO
from pydantic import BaseModel
from src.auth import AuthResponse
from src.db.postgresql import main_postgresql_cursors, get_main_postgresql_cursor
from src.helpers.socketio_helpers import send_io_client_error

class HeadingBlockUpdateInput(BaseModel):
   transaction_id: str
   id: str
   content: str

def update_heading_block(socketio: SocketIO):
    @socketio.on('update_heading_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = HeadingBlockUpdateInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute("""
                    UPDATE HeadingBlock SET text = %%s WHERE id = %%s AND user_id = %%s
                """, (
                    input.content,
                    input.id,
                    auth_info.user.id,
                ))

                socketio.emit('update_heading_block:success', id, to=transaction_id)
            except Exception as e:
                logging.error(f"Error updating heading block: {str(e)}")
                send_io_client_error(socketio, f"Error updating heading block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED update_heading_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED update_heading_block", request.sid)

class ParagraphBlockUpdateInput(BaseModel):
    transaction_id: str
    id: str
    content: str

def update_paragraph_block(socketio: SocketIO):
    @socketio.on('update_paragraph_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = ParagraphBlockUpdateInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id
                get_main_postgresql_cursor(session_id, request.sid).execute("""
                    UPDATE ParagraphBlock SET text = %%s WHERE id = %%s AND user_id = %%s
                """, (
                    input.content,
                    input.id,
                    auth_info.user.id,
                ))

                socketio.emit('update_paragraph_block:success', id, to=transaction_id)
            except Exception as e:
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED update_paragraph_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED update_paragraph_block", request.sid)


class TodoBlockUpdateInput(BaseModel):
    transaction_id: str
    id: str
    content: str


def update_todo_block(socketio: SocketIO):
    @socketio.on('update_todo_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = TodoBlockUpdateInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute("""
                    UPDATE TodoBlock SET text = %%s WHERE id = %%s AND user_id = %%s
                """, (
                    input.content,
                    input.id,
                    auth_info.user.id,
                ))

                socketio.emit('update_todo_block:success', id, to=transaction_id)
            except Exception as e:
                logging.error(f"Error updating todo block: {str(e)}")
                send_io_client_error(socketio, f"Error updating todo block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED update_todo_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED update_todo_block", request.sid)


class CodeBlockUpdateInput(BaseModel):
    transaction_id: str
    id: str
    content: str

def update_code_block(socketio: SocketIO):
    @socketio.on('update_code_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]

            transaction_id = None

            try:
                input = json.loads(str(json))
                input = CodeBlockUpdateInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute("""
                    UPDATE CodeBlock SET text = %%s WHERE id = %%s AND user_id = %%s
                """, (
                    input.content,
                    input.id,
                    auth_info.user.id,
                ))

                socketio.emit('update_code_block:success', id, to=transaction_id)
            except Exception as e:
                logging.error(f"Error updating code block: {str(e)}")
                send_io_client_error(socketio, f"Error updating code block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED update_code_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED update_code_block", request.sid)


class ListBlockUpdateInput(BaseModel):
    transaction_id: str
    id: str
    content: str


def update_list_block(socketio: SocketIO):
    @socketio.on('update_list_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = ListBlockUpdateInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute("""
                    UPDATE ListBlock SET text = %%s WHERE id = %%s AND user_id = %%s
                """, (
                    input.content,
                    input.id,
                    auth_info.user.id,
                ))

                socketio.emit('update_list_block:success', id, to=transaction_id)
            except Exception as e:
                logging.error(f"Error updating list block: {str(e)}")
                send_io_client_error(socketio, f"Error updating list block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED update_list_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED update_list_block", request.sid)

class SwapBlockInput(BaseModel):
    transaction_id: str
    block_id_1: str
    block_id_2: str

def swap_block(socketio: SocketIO):
    @socketio.on('swap_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = SwapBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute("""
                    UPDATE HeadingBlock SET block_count = %%s WHERE id = %%s AND user_id = %%s
                """, (
                    input.block_id_1,
                    input.id,
                    auth_info.user.id,
                ))

                socketio.emit('swap_block:success', id, to=transaction_id)
            except Exception as e:
                logging.error(f"Error swapping block: {str(e)}")
                send_io_client_error(socketio, f"Error swapping block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED swap_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED swap_block", request.sid)


class AddCollectionToBlockInput(BaseModel):
    transaction_id: str
    block_id: str
    collection_name: str
