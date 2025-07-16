import json
import logging
import uuid
from datetime import datetime
from flask import session, request
from flask_socketio import SocketIO
from psycopg2 import sql
from pydantic import BaseModel
from pymilvus import DataType
from configuration import conf
from src.auth import AuthResponse
from src.db.milvus import milvus_clients, get_milvus_client
from src.db.postgresql import get_main_postgresql_cursor
from src.helpers import send_io_client_error, save_base64_image

class CreateFileInput(BaseModel):
    transaction_id: str
    id: str
    file_name: str
    description: str
    folder_id: str | None
    ai_instructions: str


def create_file(socketio: SocketIO):
    @socketio.on('create_file')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]

            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = CreateFileInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id


                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            INSERT INTO File (id, user_id, name, description, total_block_count, added_to_bookmarks, ai_instructions, folder_id, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """), [
                    input.id,
                    auth_info.user.id,
                    input.file_name,
                    input.description,
                    0,
                    False,
                    input.ai_instructions,
                    input.folder_id,
                    datetime.now().timestamp(),
                    datetime.now().timestamp(),
                ])

                socketio.emit('create_file:success', input.transaction_id, to=session_id)
            except Exception as e:
                logging.error(f"Error creating file: {str(e)}")
                socketio.emit('create_file:error', transaction_id, to=session_id)
                send_io_client_error(socketio, f"Error creating file: {str(e)}", to=session_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_file: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_file", request.sid)

class CreateFolderInput(BaseModel):
    transaction_id: str
    id: str
    name: str
    description: str
    sub_folder_id: str


def create_folder(socketio: SocketIO):
    @socketio.on('create_folder')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            transaction_id = None

            try:
                session_id = session["auth_session"]
                if session_id is None:
                    raise Exception("AUTH SESSION NOT FOUND")
                auth_info: AuthResponse = session["auth_info"]

                input = json.loads(str(inputstr))
                input = CreateFolderInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            INSERT INTO FOLDER (id, user_id, name, description, sub_folder_id, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """), [
                    input.id,
                    auth_info.user.id,
                    input.name,
                    input.sub_folder_id,
                    input.description,
                    datetime.now(),
                    datetime.now(),
                ])

                socketio.emit('create_folder:success', input.transaction_id, to=session_id)
            except Exception as e:
                socketio.emit('create_folder:error', transaction_id, to=session_id)
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file: {str(e)}", session_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_folder: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_folder", request.sid)


class CreateHeadingInput(BaseModel):
    transaction_id: str
    file_id: str
    text: str
    block_count: int


def create_heading(socketio: SocketIO):
    @socketio.on('create_heading')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = CreateHeadingInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                             INSERT INTO Heading (id, user_id, file_id, text, block_count, created_at, updated_at)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """), [
                    uuid.uuid4(),
                    session_id,
                    input.file_id,
                    input.text,
                    input.block_count,
                    datetime.now(),
                    datetime.now(),
                ])

                socketio.emit('create_heading:success', transaction_id, to=session_id)
            except Exception as e:
                logging.error(f"Error creating collection: {str(e)}")
                socketio.emit('create_heading:error', transaction_id, to=session_id)
                send_io_client_error(socketio, f"Error creating collection: {str(e)}")
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_heading: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_heading", request.sid)


class CreateParagraphInput(BaseModel):
    transaction_id: str
    file_id: str
    text: str
    block_count: int


def create_paragraph(socketio: SocketIO):
    @socketio.on('create_paragraph')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]

            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = CreateParagraphInput(**input)
                input.model_dump()

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                         INSERT INTO Paragraph (id, user_id, file_id, text, block_count, created_at, updated_at)
                            VALUES (%s, %s,%s, %s, %s, %s, %s)
                        """), [
                    uuid.uuid4(),
                    auth_info.user.id,
                    input.file_id,
                    input.text,
                    input.block_count,
                    datetime.now(),
                    datetime.now(),
                ])

                socketio.emit('create_paragraph:success', input.transaction_id, to=session_id)
            except Exception as e:
                logging.error(f"Error creating collection: {str(e)}")
                socketio.emit('create_paragraph:error', transaction_id, to=session_id)
                send_io_client_error(socketio, f"Error creating collection: {str(e)}", session_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_paragraph: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_paragraph", request.sid)


class CreateFolderInput(BaseModel):
    transaction_id: str
    id: str
    name: str
    description: str
    sub_folder_id: str


def create_folder(socketio: SocketIO):
    @socketio.on('create_folder')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = CreateFolderInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            INSERT INTO FOLDER (id, user_id, name, description, sub_folder_id, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """), [
                    input.id,
                    auth_info.user.id,
                    input.name,
                    input.sub_folder_id,
                    input.description,
                    datetime.now(),
                    datetime.now(),
                ])

                socketio.emit('create_folder:success', input.transaction_id, to=session_id)
            except Exception as e:
                socketio.emit('create_folder:error', transaction_id, to=session_id)
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file", session_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_folder: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_folder", request.sid)


class CreateFileTagInput(BaseModel):
    transaction_id: str
    id: str
    name: str
    file_id: str
    block_count: int


def create_file_tag(socketio: SocketIO):
    @socketio.on('create_file_tag')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = CreateFileTagInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            INSERT INTO FileTag (id, user_id, name, file_id, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """), [
                    input.id,
                    auth_info.user.id,
                    input.name,
                    input.file_id,
                    datetime.now(),
                    datetime.now(),
                ])

                socketio.emit('create_file_tag:success', input.transaction_id, to=session_id)
            except Exception as e:
                socketio.emit('create_file_tag:error', transaction_id, to=session_id)
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file", request.sid)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_file_tag: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_file_tag", request.sid)


class CreateListBlockInput(BaseModel):
    transaction_id: str
    id: str
    name: str
    file_id: str


def create_list_block(socketio: SocketIO):
    @socketio.on('create_list_block')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = CreateListBlockInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            INSERT INTO ListBlock (id, user_id, file_id, text, block_count, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """), [
                    input.id,
                    auth_info.user.id,
                    input.file_id,
                    "",
                    input.block_count,
                    datetime.now(),
                    datetime.now(),
                ])

                socketio.emit('create_list_block:success', input.transaction_id, to=session_id)
            except Exception as e:
                socketio.emit('create_list_block:error', transaction_id, to=session_id)
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file", request.sid)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_list_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_list_block", request.sid)


class CreateImageBlockInput(BaseModel):
    transaction_id: str
    id: str
    small_description: str
    file_id: str
    block_count: int
    image: str


def create_image_block(socketio: SocketIO):
    @socketio.on('create_image_block')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = CreateImageBlockInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                save_base64_image(input.image, f"{conf.images_folder}/{input.id}")

                get_main_postgresql_cursor(session_id, request.sid).execute(sql.SQL("""
                            INSERT INTO ImageBlock (id, user_id, file_id, image_path, small_description, block_count, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """), [
                    input.id,
                    auth_info.user.id,
                    input.file_id,
                    input.small_description,
                    input.block_count,
                    datetime.now(),
                    datetime.now(),
                ])

                socketio.emit('create_image_block:success', input.transaction_id, to=session_id)
            except Exception as e:
                socketio.emit('create_image_block:error', transaction_id, to=session_id)
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file", request.sid)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_image_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_image_block", request.sid)


class CreateCollectionGroupInput(BaseModel):
    transaction_id: str
    id: str
    name: str
    description: str


def create_rag_collection_group(socketio: SocketIO):
    @socketio.on('create_rag_collection_group')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            user_id = session["user_id"]

            if session_id is None or user_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = CreateCollectionGroupInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                schema = get_milvus_client(user_id, request.sid).create_schema(
                    auto_id=False,
                    enable_dynamic_field=True,
                )

                schema.add_field(
                    name="id",
                    dtype=DataType.VARCHAR,
                    is_primary=True
                )

                schema.add_field(
                    name="id",
                    dtype=DataType.VARCHAR,
                    is_primary=True
                )

                schema.add_field(
                    field_name="vector",
                    datatype=DataType.FLOAT_VECTOR,
                    dim=1024,
                    metric_type="IP",
                )

                milvus_clients[user_id].create_collection(
                    collection_name=input.name,
                    schema=schema,
                )

                socketio.emit('create_rag_collection_group:success', input.transaction_id, to=session_id)
            except Exception as e:
                socketio.emit('create_rag_collection_group:error', transaction_id, to=session_id)
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file", request.sid)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_rag_collection_group: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_rag_collection_group", request.sid)


def add_rag_collection_to_blocks(socketio: SocketIO):
    class AddRagCollectionToBlockInput(BaseModel):
        transaction_id: str
        collection_name: str

    def add_to_block(transaction_id: str, block: str, block_table: str, collection_name: str, session_id: str,
                     sio_sid: str):
        get_main_postgresql_cursor(session_id, sio_sid).execute(sql.SQL("""
            INSERT INTO %sRagCollection (name, block_id)
            VALUES (%s, %s)
        """), [
            block_table,
            collection_name,
            block,
        ])

        socketio.emit(f'add_rag_collection_{block}:success', transaction_id, to=session_id)

    @socketio.on('add_rag_collection_heading_block')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = AddRagCollectionToBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                add_to_block(transaction_id, "heading_block", "HeadingBlock", input.collection_name, session_id,
                             request.sid)
            except Exception as e:
                logging.error(f"Error adding rag collection to block: {str(e)}")
                send_io_client_error(socketio, f"Error adding rag collection to block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED add_rag_collection_heading_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED add_rag_collection_heading_block", request.sid)

    @socketio.on('add_rag_collection_paragraph_block')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = AddRagCollectionToBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                add_to_block(transaction_id, "paragraph_block", "ParagraphBlock", input.collection_name, session_id,
                             request.sid)
            except Exception as e:
                logging.error(f"Error adding rag collection to block: {str(e)}")
                send_io_client_error(socketio, f"Error adding rag collection to block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED add_rag_collection_paragraph_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED add_rag_collection_paragraph_block", request.sid)

    @socketio.on('add_rag_collection_todo_block')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = AddRagCollectionToBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                add_to_block(transaction_id, "todo_block", "TodoBlock", input.collection_name, session_id, request.sid)
            except Exception as e:
                logging.error(f"Error adding rag collection to block: {str(e)}")
                send_io_client_error(socketio, f"Error adding rag collection to block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED add_rag_collection_todo_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED add_rag_collection_todo_block", request.sid)

    @socketio.on('add_rag_collection_image_block')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = AddRagCollectionToBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                add_to_block(transaction_id, "image_block", "ImageBlock", input.collection_name, session_id,
                             request.sid)
            except Exception as e:
                logging.error(f"Error adding rag collection to block: {str(e)}")
                send_io_client_error(socketio, f"Error adding rag collection to block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED add_rag_collection_image_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED add_rag_collection_image_block", request.sid)

    @socketio.on('add_rag_collection_list_block')
    def run(inputstr):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            transaction_id = None

            try:
                input = json.loads(str(inputstr))
                input = AddRagCollectionToBlockInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                add_to_block(transaction_id, "list_block", "ListBlock", input.collection_name, session_id, request.sid)
            except Exception as e:
                logging.error(f"Error adding rag collection to block: {str(e)}")
                send_io_client_error(socketio, f"Error adding rag collection to block: {str(e)}", transaction_id)
        except Exception as e:
            logging.error(f"UNAUTHORIZED add_rag_collection_list_block: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED add_rag_collection_list_block", request.sid)
