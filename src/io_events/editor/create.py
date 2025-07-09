import logging
import uuid
from datetime import datetime
from flask import session, request
from flask_socketio import SocketIO
from pydantic import BaseModel
from configuration import conf
from src.auth import AuthResponse
from src.db.milvus import milvus_clients
from src.db.postgresql import main_postgresql_cursors
from src.helpers.image import save_base64_image
from src.helpers.socketio_helpers import send_io_client_error

class CreateFileInput(BaseModel):
    transaction_id: str
    id: str
    file_name: str
    description: str
    folder_id: str | None
    ai_instructions: str


def create_file(socketio: SocketIO):
    @socketio.on('create_file')
    def run(json):
        session_id = session["auth_session"]
        if session_id is None:
            raise Exception("AUTH SESSION NOT FOUND")

        transaction_id = None

        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]

            input = json.loads(str(json))
            input = CreateFileInput(**input)
            input.model_dump()
            transaction_id = input.transaction_id

            file_id = uuid.uuid4()

            main_postgresql_cursors[session_id].execute("""
                INSERT INTO File (id, user_id, name, description, total_block_count, added_to_bookmarks, ai_instructions, folder_id, created_at, updated_at)
                VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)
            """, (
                file_id,
                auth_info.user.id,
                input.file_name,
                input.description,
                0,
                0,
                input.ai_instructions,
                input.folder_id,
                datetime.now(),
                datetime.now(),
            ))

            socketio.emit('create_file:success', input.transaction_id, to=session_id)
        except Exception as e:
            logging.error(f"Error creating file: {str(e)}")
            socketio.emit('create_file:error', transaction_id, to=session_id)
            send_io_client_error(socketio, f"Error creating file: {str(e)}")


class CreateFolderInput(BaseModel):
    transaction_id: str
    id: str
    name: str
    description: str
    sub_folder_id: str


def create_folder(socketio: SocketIO):
    @socketio.on('create_folder')
    def run(json):
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

                input = json.loads(str(json))
                input = CreateFolderInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                main_postgresql_cursors[session_id].execute("""
                            INSERT INTO FOLDER (id, user_id, name, description, sub_folder_id, created_at, updated_at)
                            VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s)
                        """, (
                    input.id,
                    auth_info.user.id,
                    input.name,
                    input.sub_folder_id,
                    input.description,
                    datetime.now(),
                    datetime.now(),
                ))

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
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")

            transaction_id = None

            try:
                input = json.loads(str(json))
                input = CreateHeadingInput(**input)
                input.model_dump()

                transaction_id = input.transaction_id

                main_postgresql_cursors[session["auth_session"]].execute("""
                             INSERT INTO Heading (id, user_id, file_id, text, block_count, created_at, updated_at)
                                VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s)
                            """, (
                    uuid.uuid4(),
                    session_id,
                    input.file_id,
                    input.text,
                    input.block_count,
                    datetime.now(),
                    datetime.now(),
                ))

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
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]

            transaction_id = None

            try:
                input = json.loads(str(json))
                input = CreateParagraphInput(**input)
                input.model_dump()

                main_postgresql_cursors[session["auth_session"]].execute("""
                         INSERT INTO Paragraph (id, user_id, file_id, text, block_count, created_at, updated_at)
                            VALUES (%%s, %%s,%%s, %%s, %%s, %%s, %%s)
                        """, (
                    uuid.uuid4(),
                    auth_info.user.id,
                    input.file_id,
                    input.text,
                    input.block_count,
                    datetime.now(),
                    datetime.now(),
                ))

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
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = CreateFolderInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                main_postgresql_cursors[session_id].execute("""
                            INSERT INTO FOLDER (id, user_id, name, description, sub_folder_id, created_at, updated_at)
                            VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s)
                        """, (
                    input.id,
                    auth_info.user.id,
                    input.name,
                    input.sub_folder_id,
                    input.description,
                    datetime.now(),
                    datetime.now(),
                ))

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
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = CreateFileTagInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                main_postgresql_cursors[session_id].execute("""
                            INSERT INTO FileTag (id, user_id, name, file_id, created_at, updated_at)
                            VALUES (%%s, %%s, %%s, %%s, %%s, %%s)
                        """, (
                    input.id,
                    auth_info.user.id,
                    input.name,
                    input.file_id,
                    datetime.now(),
                    datetime.now(),
                ))

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
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = CreateListBlockInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                main_postgresql_cursors[session_id].execute("""
                            INSERT INTO ListBlock (id, user_id, file_id, text, block_count, created_at, updated_at)
                            VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s)
                        """, (
                    input.id,
                    auth_info.user.id,
                    input.file_id,
                    "",
                    input.block_count,
                    datetime.now(),
                    datetime.now(),
                ))

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
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = CreateImageBlockInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                save_base64_image(input.image, f"{conf.images_folder}/{input.id}")

                main_postgresql_cursors[session_id].execute("""
                            INSERT INTO ImageBlock (id, user_id, file_id, image_path, small_description, block_count, created_at, updated_at)
                            VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)
                        """, (
                    input.id,
                    auth_info.user.id,
                    input.file_id,
                    input.small_description,
                    input.block_count,
                    datetime.now(),
                    datetime.now(),
                ))

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
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = CreateCollectionGroupInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                main_postgresql_cursors[session_id].execute("""
                INSERT INTO RagCollectionGroup (id, user_id, name, description, created_at, updated_at)
                VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s)
                """, (
                    input.id,
                    auth_info.user.id,
                    input.name,
                    input.description,
                    datetime.now(),
                    datetime.now(),
                ))

                milvus_clients[session_id].create_collection(
                    collection_name=input.name,
                    dimension=1024,
                    metric_type="IP",
                    id_type='VARCHAR',
                )

                socketio.emit('create_rag_collection_group:success', input.transaction_id, to=session_id)

            except Exception as e:
                socketio.emit('create_rag_collection_group:error', transaction_id, to=session_id)
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file", request.sid)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_rag_collection_group: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_rag_collection_group", request.sid)


class RagCollectionInput(BaseModel):
    transaction_id: str
    id: str
    group_id: str
    name: str
    metadata: str
    block_id: str

def create_rag_collection(socketio: SocketIO):
    def create_rag_collection_in_db(input: RagCollectionInput, session_id: str, auth_info: AuthResponse,
                                    block_name: str):
        main_postgresql_cursors[session_id].execute("""
                        INSERT INTO RagCollection (%%s, id, user_id, group_id, name, metadata, created_at, updated_at)
                        VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)
                        """, (
            block_name,
            input.block_id,
            input.id,
            auth_info.user.id,
            input.group_id,
            input.name,
            input.metadata,
            datetime.now(),
            datetime.now(),
        ))

    @socketio.on('create_rag_collection:heading_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = RagCollectionInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                create_rag_collection_in_db(input, session_id, auth_info, "heading_block_id")

                socketio.emit('create_rag_collection:success', input.transaction_id, to=session_id)
            except Exception as e:
                socketio.emit('create_rag_collection:error', transaction_id, to=session_id)
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file", request.sid)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_rag_collection: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_rag_collection", request.sid)

    @socketio.on('create_rag_collection:paragraph_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = RagCollectionInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                create_rag_collection_in_db(input, session_id, auth_info, "paragraph_block_id")

                socketio.emit('create_rag_collection:success', input.transaction_id, to=session_id)
            except Exception as e:
                socketio.emit('create_rag_collection:error', transaction_id, to=session_id)
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file", request.sid)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_rag_collection: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_rag_collection", request.sid)

    @socketio.on('create_rag_collection:code_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = RagCollectionInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                create_rag_collection_in_db(input, session_id, auth_info, "code_block_id")

                socketio.emit('create_rag_collection:success', input.transaction_id, to=session_id)
            except Exception as e:
                socketio.emit('create_rag_collection:error', transaction_id, to=session_id)
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file", request.sid)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_rag_collection: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_rag_collection", request.sid)

    @socketio.on('create_rag_collection:list_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = RagCollectionInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                create_rag_collection_in_db(input, session_id, auth_info, "list_block_id")

                socketio.emit('create_rag_collection:success', input.transaction_id, to=session_id)
            except Exception as e:
                socketio.emit('create_rag_collection:error', transaction_id, to=session_id)
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file", request.sid)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_rag_collection: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_rag_collection", request.sid)

    @socketio.on('create_rag_collection:todo_block')
    def run(json):
        try:
            session_id = session["auth_session"]
            if session_id is None:
                raise Exception("AUTH SESSION NOT FOUND")
            auth_info: AuthResponse = session["auth_info"]
            transaction_id = None

            try:
                input = json.loads(str(json))
                input = RagCollectionInput(**input)
                input.model_dump()
                transaction_id = input.transaction_id

                create_rag_collection_in_db(input, session_id, auth_info, "todo_block_id")

                socketio.emit('create_rag_collection:success', input.transaction_id, to=session_id)
            except Exception as e:
                socketio.emit('create_rag_collection:error', transaction_id, to=session_id)
                logging.error(f"Error creating file: {str(e)}")
                send_io_client_error(socketio, f"Error creating file", request.sid)
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_rag_collection: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_rag_collection", request.sid)
