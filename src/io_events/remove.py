import logging
import os.path

from flask import session, request
from flask_socketio import SocketIO
from psycopg2 import sql
from pydantic import BaseModel

from src.auth import AuthResponse
from src.db.milvus import get_milvus_client
from src.db.postgresql import get_main_postgresql_cursor
from src.helpers import send_io_client_error


class RemoveHeadingBlockInput(BaseModel):
    transaction_id: str
    id: str


def remove_heading_block(socketio: SocketIO):
    @socketio.on('remove_heading_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = RemoveHeadingBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                    DELETE FROM HeadingBlock WHERE id = %s AND user_id = %s
                """), [
                    input.id,
                    auth_info.user.id,
                ])

                socketio.emit('remove_heading_block:success', id, to=transaction_id)
            except Exception as e:
                logging.error(f"Error removing heading block: {str(e)}")
                send_io_client_error(socketio, f"Error removing heading block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED remove_heading_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED remove_heading_block", request.sid)


class RemoveParagraphBlockInput(BaseModel):
    transaction_id: str
    id: str


def remove_paragraph_block(socketio: SocketIO):
    @socketio.on('remove_paragraph_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = RemoveParagraphBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                    DELETE FROM ParagraphBlock WHERE id = %s AND user_id = %s
                """), [
                    input.id,
                    auth_info.user.id,
                ])

                socketio.emit('remove_paragraph_block:success', id, to=transaction_id)
            except Exception as e:
                logging.error(f"Error removing paragraph block: {str(e)}")
                send_io_client_error(socketio, f"Error removing paragraph block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED remove_paragraph_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED remove_paragraph_block", request.sid)


class RemoveTodoBlockInput(BaseModel):
    transaction_id: str
    id: str


def remove_todo_block(socketio: SocketIO):
    @socketio.on('remove_todo_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = RemoveTodoBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                    DELETE FROM TodoBlock WHERE id = %s AND user_id = %s
                """), [
                    input.id,
                    auth_info.user.id,
                ])

                socketio.emit('remove_todo_block:success', id, to=transaction_id)
            except Exception as e:
                logging.error(f"Error removing todo block: {str(e)}")
                send_io_client_error(socketio, f"Error removing todo block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED remove_todo_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED remove_todo_block", request.sid)


class RemoveCodeBlockInput(BaseModel):
    transaction_id: str
    id: str


def remove_code_block(socketio: SocketIO):
    @socketio.on('remove_code_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = RemoveCodeBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                    DELETE FROM CodeBlock WHERE id = %s AND user_id = %s
                """), [
                    input.id,
                    auth_info.user.id,
                ])

                socketio.emit('remove_code_block:success', id, to=transaction_id)
            except Exception as e:
                logging.error(f"Error removing code block: {str(e)}")
                send_io_client_error(socketio, f"Error removing code block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED remove_code_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED remove_code_block", request.sid)


class RemoveListBlockInput(BaseModel):
    transaction_id: str
    id: str


def remove_list_block(socketio: SocketIO):
    @socketio.on('remove_list_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = RemoveListBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                    DELETE FROM ListBlock WHERE id = %s AND user_id = %s
                """), [
                    input.id,
                    auth_info.user.id,
                ])

                socketio.emit('remove_list_block:success', id, to=transaction_id)
            except Exception as e:
                logging.error(f"Error removing list block: {str(e)}")
                send_io_client_error(socketio, f"Error removing list block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED remove_list_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED remove_list_block", request.sid)


class RemoveImageBlockInput(BaseModel):
    transaction_id: str
    id: str


def remove_image_block(socketio: SocketIO):
    @socketio.on('remove_image_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = RemoveImageBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                image_path = get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                    SELECT image_path FROM ImageBlock WHERE id = %s AND user_id = %s
                """), [
                    input.id,
                    auth_info.user.id,
                ])
                image_path_records = get_main_postgresql_cursor(session_id, request.sid).fetchone()
                logging.info(f"Image path: {image_path}")

                if os.path.exists(image_path_records[0].image_path):
                    os.remove(image_path_records[0].image_path)

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                    DELETE FROM ImageBlock WHERE id = %s AND user_id = %s
                """), [
                    input.id,
                    auth_info.user.id,
                ])

                socketio.emit('remove_image_block:success', id, to=transaction_id)
            except Exception as e:
                logging.error(f"Error removing image block: {str(e)}")
                send_io_client_error(socketio, f"Error removing image block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED remove_image_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED remove_image_block", request.sid)


def remove_rag_collection_from_blocks(socketio: SocketIO):
    class RemoveRagCollectionFromBlockInput(BaseModel):
        transaction_id: str
        block_id: str
        collection_name: str

    def remove_from_block(transaction_id: str, block: str, block_table: str, collection_name: str, user_id: str,
                          sio_sid: str, session_id: str):
        get_main_postgresql_cursor(session_id, sio_sid).execute(sql.SQL("""
            DELETE FROM %sRagCollection WHERE name = %s AND block_id = %s
        """), [
            block_table,
            collection_name,
            block,
        ])

        get_milvus_client(user_id, sio_sid).drop_collection(collection_name)

        socketio.emit(f'remove_rag_collection_{block}:success', transaction_id, to=session_id)

    @socketio.on('remove_rag_collection_heading_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            user_id = session["user_id"]

            if session_id is None or user_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = RemoveRagCollectionFromBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                remove_from_block(transaction_id, "heading_block", "HeadingBlock", input.collection_name, user_id,
                                  request.sid,
                                  session_id)
            except Exception as e:
                logging.error(f"Error removeing rag collection to block: {str(e)}")
                send_io_client_error(socketio, f"Error removeing rag collection to block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED remove_rag_collection_heading_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED remove_rag_collection_heading_block", request.sid)

    @socketio.on('remove_rag_collection_paragraph_block')
    def remove_rag_collection_paragraph_block(input):
        try:
            auth_session = session["auth_session"]
            user_id = session["user_id"]
            session_id = session["session_id"]

            try:
                transaction_id = input.transaction_id

                remove_from_block(transaction_id, "paragraph_block", "ParagraphBlock", input.collection_name, user_id,
                                  request.sid,
                                  session_id)
            except Exception as e:
                logging.error(f"Error removeing rag collection to block: {str(e)}")
                send_io_client_error(socketio, f"Error removeing rag collection to block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED remove_rag_collection_paragraph_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED remove_rag_collection_paragraph_block", request.sid)

    @socketio.on('remove_rag_collection_list_block')
    def remove_rag_collection_list_block(input):
        try:
            auth_session = session["auth_session"]
            user_id = session["user_id"]
            session_id = session["session_id"]

            try:
                transaction_id = input.transaction_id

                remove_from_block(transaction_id, "list_block", "ListBlock", input.collection_name, user_id,
                                  request.sid,
                                  session_id)
            except Exception as e:
                logging.error(f"Error removeing rag collection to block: {str(e)}")
                send_io_client_error(socketio, f"Error removeing rag collection to block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED remove_rag_collection_list_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED remove_rag_collection_list_block", request.sid)
