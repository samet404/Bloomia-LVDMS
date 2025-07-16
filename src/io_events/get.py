import json
import logging

from flask import session, request
from flask_socketio import SocketIO
from psycopg2 import sql
from pydantic import BaseModel
from src.helpers.socketio_helpers import send_io_client_error

from src.auth import AuthResponse
from src.db.postgresql import get_main_postgresql_cursor


class GetFilesInput(BaseModel):
    transaction_id: str


def get_files(socketio: SocketIO):
    @socketio.on('get_files')
    def run(input_str):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]

            try:
                input = json.loads(str(input_str))
                input = GetFilesInput(**input)
                input.model_dump()

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            SELECT * FROM File WHERE user_id = %s
                        """), [
                    auth_info.user.id,
                ])

                files = get_main_postgresql_cursor(session_id, request.sid).fetchall()

                socketio.emit('get_files', files, to=session_id)
                socketio.emit('get_files:success', input.transaction_id, to=session_id)
            except Exception as e:
                logging.error(f"Error getting files: {str(e)}")
                send_io_client_error(socketio, f"Error getting files: {str(e)}", session_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED get_files: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED get_files", request.sid)


class GetFoldersInput(BaseModel):
    transaction_id: str


def get_folders(socketio: SocketIO):
    @socketio.on('get_folders')
    def run(input_str):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]

            try:
                input = json.loads(str(input_str))
                input = GetFoldersInput(**input)
                input.model_dump()

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            SELECT * FROM Folder WHERE user_id = %s
                        """), [
                    auth_info.user.id,
                ])

                folders = get_main_postgresql_cursor(session_id, request.sid).fetchall()

                socketio.emit('get_folders', folders, to=session_id)
                socketio.emit('get_folders:success', input.transaction_id, to=session_id)
            except Exception as e:
                logging.error(f"Error getting folders: {str(e)}")
                send_io_client_error(socketio, f"Error getting folders: {str(e)}", session_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED get_folders: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED get_folders", request.sid)


class GetBlockByCountAndFileIdInput(BaseModel):
    transaction_id: str
    file_id: str
    block_count: int


def get_block_by_count_and_file_id(socketio: SocketIO):
    @socketio.on('get_block_by_count_and_file_id')
    def run(input_str):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(input_str))
                input = GetFilesInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            SELECT * FROM HeadingBlock WHERE user_id = %s AND file_id = %s AND block_count = %s
                        """), [
                    auth_info.user.id,
                    input.file_id,
                    input.block_count,
                ])
                heading_block = get_main_postgresql_cursor(session_id, request.sid).fetchone()
                if heading_block is not None:
                    socketio.emit('get_block_by_count_and_file_id:heading_block', heading_block, to=session_id)
                    socketio.emit('get_block_by_count_and_file_id:success', input.transaction_id, to=session_id)

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            SELECT * FROM ParagraphBlock WHERE user_id = %s AND file_id = %s AND block_count = %s
                        """), [
                    auth_info.user.id,
                    input.file_id,
                    input.block_count,
                ])
                paragraph_block = get_main_postgresql_cursor(session_id, request.sid).fetchone()
                if paragraph_block is not None:
                    socketio.emit('get_block_by_count_and_file_id:paragraph_block', paragraph_block, to=session_id)
                    socketio.emit('get_block_by_count_and_file_id:success', input.transaction_id, to=session_id)

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            SELECT * FROM TodoBlock WHERE user_id = %s AND file_id = %s AND block_count = %s
                        """), [
                    auth_info.user.id,
                    input.file_id,
                    input.block_count,
                ])
                todo_block = get_main_postgresql_cursor(session_id, request.sid).fetchone()
                if todo_block is not None:
                    socketio.emit('get_block_by_count_and_file_id:todo_block', todo_block, to=session_id)
                    socketio.emit('get_block_by_count_and_file_id:success', input.transaction_id, to=session_id)

                socketio.emit('get_block_by_count_and_file_id:error', transaction_id, to=session_id)

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            SELECT * FROM CodeBlock WHERE user_id = %s AND file_id = %s AND block_count = %s
                        """), [
                    auth_info.user.id,
                    input.file_id,
                    input.block_count,
                ])
                code_block = get_main_postgresql_cursor(session_id, request.sid).fetchone()
                if code_block is not None:
                    socketio.emit('get_block_by_count_and_file_id:code_block', code_block, to=session_id)
                    socketio.emit('get_block_by_count_and_file_id:success', input.transaction_id, to=session_id)

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            SELECT * FROM ListBlock WHERE user_id = %s AND file_id = %s AND block_count = %s
                        """), [
                    auth_info.user.id,
                    input.file_id,
                    input.block_count,
                ])
                list_block = get_main_postgresql_cursor(session_id, request.sid).fetchone()
                if list_block is not None:
                    socketio.emit('get_block_by_count_and_file_id:list_block', list_block, to=session_id)
                    socketio.emit('get_block_by_count_and_file_id:success', input.transaction_id, to=session_id)

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            SELECT * FROM ImageBlock WHERE user_id = %s AND file_id = %s AND block_count = %s
                        """), [
                    auth_info.user.id,
                    input.file_id,
                    input.block_count,
                ])
                image_block = get_main_postgresql_cursor(session_id, request.sid).fetchone()
                if image_block is not None:
                    socketio.emit('get_block_by_count_and_file_id:image_block', image_block, to=session_id)
                    socketio.emit('get_block_by_count_and_file_id:success', input.transaction_id, to=session_id)

                socketio.emit('get_block_by_count_and_file_id:error', transaction_id, to=session_id)
            except Exception as e:
                logging.error(f"Error getting files: {str(e)}")
                socketio.emit('get_block_by_count_and_file_id:error', transaction_id, to=session_id)
                send_io_client_error(socketio, f"Error getting files: {str(e)}", session_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED get_files: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED get_files", request.sid)
