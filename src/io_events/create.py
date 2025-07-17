import json
import logging
from datetime import datetime

from flask import session, request
from flask_socketio import SocketIO
from psycopg2 import sql
from pydantic import BaseModel
from pymilvus import DataType

from configuration import conf
from src.db.milvus import get_milvus_client
from src.db.postgresql import get_main_postgresql_cursor
from src.helpers import save_base64_image, ErrorResponse, event_err_client, event_loading_client, LoadingResponse, \
    event_success_client, SuccessResponse, event_err_server, safe_parse_event_input, \
    send_auth_err_if_one_of_is_none


def create_file(socketio: SocketIO):
    class CreateFileInput(BaseModel):
        transaction_id: str
        id: str
        file_name: str
        description: str
        folder_id: str | None
        ai_instructions: str

    event_name = 'create_file'

    @socketio.on(event_name)
    def run(inputstr):
        user_id = session.get("user_id", None)
        if send_auth_err_if_one_of_is_none(socketio, request.sid, event_name, user_id):
            return

        input = safe_parse_event_input(socketio, request.sid, event_name, CreateFileInput, inputstr)
        if input is None:
            return

        try:
            event_loading_client(socketio, event_name, user_id, LoadingResponse(transaction_id=input.transaction_id))

            get_main_postgresql_cursor(user_id, request.sid).execute(sql.SQL("""
                            INSERT INTO File (id, user_id, name, description, total_block_count, added_to_bookmarks, ai_instructions, folder_id, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """), [
                input.id,
                input.file_name,
                input.description,
                0,
                False,
                input.ai_instructions,
                input.folder_id,
                datetime.now().timestamp(),
                datetime.now().timestamp(),
            ])

            event_success_client(socketio, event_name, user_id, SuccessResponse(transaction_id=input.transaction_id))
        except Exception:
            event_err_server(event_name)
            event_err_client(socketio, event_name, user_id,
                             ErrorResponse(code="INTERNAL", transaction_id=input.transaction_id))


def create_folder(socketio: SocketIO):
    class CreateFolderInput(BaseModel):
        transaction_id: str
        id: str
        name: str
        description: str
        sub_folder_id: str

    event_name = 'create_folder'

    @socketio.on(event_name)
    def run(inputstr):
        user_id: str = session.get("user_id", None)
        if send_auth_err_if_one_of_is_none(socketio, request.sid, event_name, user_id):
            return

        input = safe_parse_event_input(socketio, request.sid, event_name, CreateFolderInput, inputstr)
        if input is None:
            return

        try:
            event_loading_client(socketio, event_name, user_id, LoadingResponse(transaction_id=input.transaction_id))
            get_main_postgresql_cursor(request.sid).execute(sql.SQL("""
                            INSERT INTO FOLDER (id, user_id, name, description, sub_folder_id, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """), [
                input.id,
                user_id,
                input.name,
                input.sub_folder_id,
                input.description,
                datetime.now(),
                datetime.now(),
            ])
            event_success_client(socketio, event_name, user_id, SuccessResponse(transaction_id=input.transaction_id))
        except Exception:
            event_err_server(event_name)
            event_err_client(socketio, event_name, user_id, ErrorResponse(code="INTERNAL"))


def create_heading(socketio: SocketIO):
    class CreateHeadingInput(BaseModel):
        transaction_id: str
        id: str
        file_id: str
        text: str
        block_count: int

    event_name = 'create_heading'

    @socketio.on(event_name)
    def run(inputstr):
        user_id: str = session.get("user_id", None)
        if send_auth_err_if_one_of_is_none(socketio, request.sid, event_name, user_id):
            return

        input = safe_parse_event_input(socketio, request.sid, event_name, CreateHeadingInput, inputstr)
        if input is None:
            return

        try:
            event_loading_client(socketio, event_name, user_id, LoadingResponse(transaction_id=input.transaction_id))
            get_main_postgresql_cursor(request.sid).execute(sql.SQL("""
                         INSERT INTO Heading (id, user_id, file_id, text, block_count, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """), [
                input.id,
                user_id,
                input.file_id,
                input.text,
                input.block_count,
                datetime.now(),
                datetime.now(),
            ])

            event_success_client(socketio, event_name, user_id, SuccessResponse(transaction_id=input.transaction_id))
        except Exception:
            event_err_server(event_name)
            event_err_client(socketio, event_name, user_id, ErrorResponse(code="INTERNAL"))


def create_paragraph(socketio: SocketIO):
    class CreateParagraphInput(BaseModel):
        transaction_id: str
        id: str
        file_id: str
        text: str
        block_count: int

    event_name = 'create_paragraph'

    @socketio.on(event_name)
    def run(inputstr):
        user_id: str = session.get("user_id", None)
        if send_auth_err_if_one_of_is_none(socketio, request.sid, event_name, user_id):
            return

        input = safe_parse_event_input(socketio, request.sid, event_name, CreateParagraphInput, inputstr)
        if input is None:
            return

        try:
            event_loading_client(socketio, event_name, user_id, LoadingResponse(transaction_id=input.transaction_id))

            date = datetime.now().timestamp()
            get_main_postgresql_cursor(request.sid).execute(sql.SQL("""
                     INSERT INTO Paragraph (id, user_id, file_id, text, block_count, created_at, updated_at)
                     VALUES (%s, %s,%s, %s, %s, %s, %s)
                    """), [
                input.id,
                user_id,
                input.file_id,
                input.text,
                input.block_count,
                date,
                date,
            ])

            event_success_client(socketio, event_name, user_id, SuccessResponse(transaction_id=input.transaction_id))
        except Exception:
            event_err_server(event_name)
            event_err_client(socketio, event_name, user_id,
                             ErrorResponse(code="INTERNAL", transaction_id=input.transaction_id))


def create_file_tag(socketio: SocketIO):
    class CreateFileTagInput(BaseModel):
        transaction_id: str
        id: str
        name: str
        file_id: str
        block_count: int

    event_name = 'create_file_tag'

    @socketio.on(event_name)
    def run(inputstr):
        user_id: str = session.get("user_id", None)
        if send_auth_err_if_one_of_is_none(socketio, request.sid, event_name, user_id):
            return

        input = safe_parse_event_input(socketio, request.sid, event_name, CreateFileTagInput, inputstr)
        if input is None:
            return

        try:
            event_loading_client(socketio, event_name, user_id, LoadingResponse(transaction_id=input.transaction_id))
            get_main_postgresql_cursor(request.sid).execute(sql.SQL("""
                            INSERT INTO FileTag (id, user_id, name, file_id, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """), [
                input.id,
                user_id,
                input.name,
                input.file_id,
                datetime.now(),
                datetime.now(),
            ])

            event_success_client(socketio, event_name, user_id, SuccessResponse(transaction_id=input.transaction_id))
        except Exception as e:
            event_err_server(event_name)
            event_err_client(socketio, event_name, user_id,
                             ErrorResponse(code="INTERNAL", transaction_id=input.transaction_id))


def create_list_block(socketio: SocketIO):
    class CreateListBlockInput(BaseModel):
        transaction_id: str
        id: str
        name: str
        file_id: str

    event_name = 'create_list_block'

    @socketio.on(event_name)
    def run(inputstr):
        user_id: str = session.get("user_id", None)
        if send_auth_err_if_one_of_is_none(socketio, request.sid, event_name, user_id):
            return

        input = safe_parse_event_input(socketio, request.sid, event_name, CreateListBlockInput, inputstr)
        if input is None:
            return

        try:
            event_loading_client(socketio, event_name, user_id, LoadingResponse(transaction_id=input.transaction_id))

            get_main_postgresql_cursor(request.sid).execute(sql.SQL("""
                            INSERT INTO ListBlock (id, user_id, file_id, text, block_count, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """), [
                input.id,
                user_id,
                input.file_id,
                "",
                input.block_count,
                datetime.now(),
                datetime.now(),
            ])

            event_success_client(socketio, event_name, user_id, SuccessResponse(transaction_id=input.transaction_id))
        except Exception:
            event_err_server(event_name)
            event_err_client(socketio, event_name, user_id,
                             ErrorResponse(code="INTERNAL", transaction_id=input.transaction_id))


def create_image_block(socketio: SocketIO):
    class CreateImageBlockInput(BaseModel):
        transaction_id: str
        id: str
        small_description: str
        file_id: str
        block_count: int
        image: str

    event_name = 'create_image_block'

    @socketio.on(event_name)
    def run(inputstr):
        user_id: str = session.get("user_id", None)
        if send_auth_err_if_one_of_is_none(socketio, request.sid, event_name, user_id):
            return

        input = safe_parse_event_input(socketio, request.sid, event_name, CreateImageBlockInput, inputstr)
        if input is None:
            return

        try:
            event_loading_client(socketio, event_name, user_id, LoadingResponse(transaction_id=input.transaction_id))

            save_base64_image(input.image, f"{conf.images_folder}/{input.id}")
            get_main_postgresql_cursor(request.sid).execute(sql.SQL("""
                            INSERT INTO ImageBlock (id, user_id, file_id, image_path, small_description, block_count, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """), [
                input.id,
                user_id,
                input.file_id,
                input.small_description,
                input.block_count,
                datetime.now(),
                datetime.now(),
            ])

            event_success_client(socketio, event_name, user_id, SuccessResponse(transaction_id=input.transaction_id))
        except Exception:
            event_err_server(event_name)
            event_err_client(socketio, event_name, user_id,
                             ErrorResponse(code="INTERNAL", transaction_id=input.transaction_id))


def create_rag_collection_group(socketio: SocketIO):
    class CreateCollectionGroupInput(BaseModel):
        transaction_id: str
        id: str
        name: str
        description: str

    event_name = 'create_rag_collection_group'

    @socketio.on(event_name)
    def run(inputstr):
        user_id = session.get("user_id", None)
        if send_auth_err_if_one_of_is_none(socketio, request.sid, event_name, user_id):
            return

        input = safe_parse_event_input(socketio, request.sid, event_name, CreateCollectionGroupInput, inputstr)
        if input is None:
            return

        try:
            event_loading_client(socketio, event_name, user_id, LoadingResponse(transaction_id=input.transaction_id))

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

            get_milvus_client(request.sid, user_id).create_collection(
                collection_name=input.name,
                schema=schema,
            )

            event_success_client(socketio, event_name, user_id, SuccessResponse(transaction_id=input.transaction_id))
        except Exception:
            event_err_server(event_name)
            event_err_client(socketio, event_name, user_id,
                             ErrorResponse(code="INTERNAL", transaction_id=input.transaction_id))


def add_rag_collection_to_blocks(socketio: SocketIO):
    class AddRagCollectionToBlockInput(BaseModel):
        transaction_id: str
        id: str
        collection_name: str

    def add_to_block(event_name: str, transaction_id: str, sql_rag_block_table_name: str, collection_name: str,
                     block_id: str,
                     user_id: str, sio_sid: str):
        event_loading_client(socketio, event_name, user_id,
                             LoadingResponse(transaction_id=transaction_id))

        get_main_postgresql_cursor(sio_sid).execute(sql.SQL("""
            INSERT INTO {table} (name, block_id)
            VALUES (%s, %s)
        """).format(table=sql.Identifier(sql_rag_block_table_name)), [
            collection_name,
            block_id,
        ])

        event_success_client(socketio, event_name, user_id,
                             SuccessResponse(transaction_id=transaction_id))

    event_name_heading = 'add_rag_collection_heading_block'

    @socketio.on(event_name_heading)
    def run(inputstr):
        user_id: str = session.get("user_id", None)
        if send_auth_err_if_one_of_is_none(socketio, request.sid, event_name_heading, user_id):
            return

        input = safe_parse_event_input(socketio, request.sid, event_name_heading, AddRagCollectionToBlockInput,
                                       inputstr)
        if input is None:
            return

        try:
            add_to_block(event_name_heading, input.transaction_id, "HeadingBlockRagCollection",
                         input.collection_name, input.id, user_id, request.sid)
        except Exception:
            event_err_server(event_name_heading)
            event_err_client(socketio, event_name_heading, user_id,
                             ErrorResponse(code="INTERNAL", transaction_id=input.transaction_id))

    event_name_paragraph = 'add_rag_collection_paragraph_block'
    @socketio.on(event_name_paragraph)
    def run(inputstr):
        user_id: str = session.get("user_id", None)
        if send_auth_err_if_one_of_is_none(socketio, request.sid, event_name_heading, user_id):
            return

        input = safe_parse_event_input(socketio, request.sid, event_name_heading, AddRagCollectionToBlockInput,
                                       inputstr)
        if input is None:
            return

        try:
            add_to_block(event_name_heading, input.transaction_id, "ParagraphBlockRagCollection",
                         input.collection_name, input.id, user_id, request.sid)

        except Exception:
            event_err_server(event_name_heading)
            event_err_client(socketio, event_name_heading, user_id,
                             ErrorResponse(code="INTERNAL", transaction_id=input.transaction_id))

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
