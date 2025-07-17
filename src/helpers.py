# ====== Helper functions for tasks related to server logic itself rather than utility

import base64
import json
import logging
from enum import Enum
from io import BytesIO
from textwrap import dedent
from typing import TypeVar
from PIL import Image
from flask_socketio import SocketIO
from psycopg2 import sql
from psycopg2.extensions import cursor
from pydantic import BaseModel
from src.utils import detailed_exception_info

T = TypeVar('T')

def send_auth_err_if_one_of_is_none(sio: SocketIO, sio_id: str, event_name: str, *args):
    """
    Logs auth error response, returns True if any of the arguments is None.
    This is used to check if the user is authorized for an event.
    """
    if any(arg is None for arg in args):
        event_err_server(f"{event_name} unauthorized error")
        event_err_client(sio, event_name, sio_id, ErrorResponse(code="UNAUTHORIZED"))
        return True
    return False

def safe_parse_pydantic_model(model_class, data):
    """
    Safely parses data into a Pydantic model, returning None if parsing fails.
    """
    try:
        return model_class(**data)
    except Exception:
        return None

def safe_parse_event_input(sio: SocketIO, sio_id: str, event_name: str, model_class: T, input: any) -> T | None:
    """
    Safely parses data into a Pydantic model, returning None and logging an error if parsing fails.
    """
    try:
        json_data = json.loads(str(input))
        return model_class(json_data)
    except Exception:
        event_err_server(f"{event_name} input parsing error")
        event_err_client(sio, event_name, sio_id, ErrorResponse(code="INVALID_INPUT"))

        return None

def unauthorized_err_server(event_name: str, session_id: str):
    """
    Logs an unauthorized error for a specific event.
    """
    logging.error(f"{session_id} UNAUTHORIZED: {event_name}")

def event_err_server(extra: str):
    logging.error(detailed_exception_info(extra))

class ServerErrorResponse(BaseModel):
    transaction_id: str | None = None
    code: str
    message: str

class ErrorResponse(BaseModel):
    code: str
    transaction_id: str | None = None

def convert_server_err_to_client_err(server_error: ServerErrorResponse) -> ErrorResponse:
    """
    Converts a server error response to a client error response.
    """
    return ErrorResponse(
        code=server_error.code,
        transaction_id=server_error.transaction_id
    )

def event_err_client(socketio: SocketIO, event: str, session_id: str, response: ErrorResponse):
    """
    Sends an error response to the client.
    """
    socketio.emit(f"{event}:error", response.model_dump_json(), to=session_id)

class LoadingResponse(BaseModel):
    transaction_id: str | None = None

def event_loading_client(socketio: SocketIO, event: str, session_id: str, loading_response: LoadingResponse):
    """
    Sends a loading response to the client.
    """
    socketio.emit(f"{event}:loading", loading_response.model_dump_json(), to=session_id)

class SuccessResponse(BaseModel):
    transaction_id: str | None = None

def event_success_client(socketio: SocketIO, event: str, session_id: str, success_response: SuccessResponse):
    """
    Sends a success response to the client.
    """
    socketio.emit(f"{event}:success", success_response.model_dump_json(), to=session_id)

class Persona(Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    CALM = "calm"
    CONFUSED = "confused"
    SURPRISED = "surprised"
    FEMININE = "feminine"
    MASCULINE = "masculine"
    NEUTRAL = "neutral"

def get_fix_grammar_prompt(text: str):
    return dedent(
        f"""
        SYSTEM INSTRUCTIONS:
        You are helpful assistant that fixes the grammar in the given text.
        Your task is to fix the grammar in the given text.
        Please don't add any extra text. Don't change meaning of text. Don't add your comments to response. Only fix the grammer.
        Your responses shouldn't start and end with quotes.
        Text:
        {text}
        """
    ).strip()


def get_fix_spelling_prompt(text: str):
    return dedent(
        f"""
        SYSTEM INSTRUCTIONS:
        You are helpful assistant that fixes the spelling in the given text.
        Your task is to fix the spelling in the given text.
        Please don't add any extra text. Don't change meaning of text. Don't add your comments to response. Only fix the spelling.
        Your responses shouldn't start and end with quotes.
        Text:
        {text}
        """
    ).strip()


def get_change_persona_prompt(text: str, persona: Persona | str):
    persona_definition = ""
    if persona == Persona.FEMININE:
        persona_definition = "Rewrite the following text with a more feminine persona. Focus on conveying a tone that is warm, empathetic, and perhaps a bit more expressive, while maintaining clarity and professionalism where needed. Avoid stereotypes, but lean into qualities often associated with feminine communication styles."
    elif persona == Persona.MASCULINE:
        persona_definition = "Rewrite the following text, imbuing it with a masculine persona. Focus on directness, confidence, and a practical tone. Avoid excessive emotionality or overly flowery language. Make it sound strong and assertive."
    elif persona == Persona.NEUTRAL:
        persona_definition = "Transform the persona of the given text to be strictly objective. Ensure all statements are presented as verifiable facts or commonly accepted information, devoid of personal interpretation or sentiment. Maintain an even and balanced tone throughout."
    elif persona == Persona.ANGRY:
        persona_definition = "Rewrite the following text with an angry persona. The tone should be frustrated, indignant, and convey strong displeasure. Use more forceful language and perhaps some exclamations, but avoid profanity."
    elif persona == Persona.SAD:
        persona_definition = "Please rewrite the following text, infusing it with a sad and melancholic persona. Focus on conveying feelings of sorrow, dejection, and perhaps a sense of loss or hopelessness, without being overly dramatic. Use somber language and imagery where appropriate."
    elif persona == Persona.CONFUSED:
        persona_definition = "Rewrite the following text from the perspective of someone who is utterly confused and trying to make sense of things. They should frequently use hesitant language, express uncertainty, and perhaps ask rhetorical questions."
    elif persona == Persona.SURPRISED:
        persona_definition = "Transform the given text to reflect a persona that is genuinely surprised, as if encountering something unexpected but not necessarily shocking. Focus on expressions of wonder and mild disbelief."
    elif persona == Persona.CALM:
        persona_definition = "Transform the tone of this text to be serene, tranquil, and reassuring. Avoid any hint of urgency or excitement"

    return dedent(
        f"""
        SYSTEM INSTRUCTIONS:
        You are helpful assistant that changes persona in the given text.
        Your task is to change persona in the given text. Don't change general meaning of text.
        Your responses shouldn't start and end with quotes.
        Persona directive: {persona_definition}
        Text: {text}
        """
    ).strip()


def get_summarize_prompt(text: str):
    return dedent(
        f"""
        SYSTEM INSTRUCTIONS:
        You are helpful assistant that summarizes the given text.
        Your task is to summarize the given text.
        Your responses shouldn't start and end with quotes.
        Text: {text}
        """
    ).strip()


def get_simplify_text_prompt(text: str):
    return dedent(
        f"""
        SYSTEM INSTRUCTIONS:
        You are helpful assistant that simplifies the given text.
        Your task is to simplify the given text.
        Your responses shouldn't start and end with quotes.
        Text: {text}
        """
    ).strip()


def get_target_audiences_prompt(text: str, tag_count: int):
    return dedent(
        f"""
        SYSTEM INSTRUCTIONS:
        You are helpful assistant that generates tags that represents possible target audience of provided text.
        Your task is to generate tags that represents possible target audience of provided text.
        Tags should be separated with commas with no space. Your response shouldn't start and end with quotes. 
        Example response with irrelevant tags: People interested in history,Students of computer science,Mathematicians,People interested in Alan Turing,People interested in algorithms,People interested in cryptography,Logicians,Philosophers,Biologists,People interested in theoretical biology 
        Generate {tag_count} tags for the given text.
        Text: {text}
        """
    ).strip()


def get_generate_questions_prompt(text: str, question_count: int):
    return dedent(
        f"""
        SYSTEM INSTRUCTIONS:
        You are helpful assistant that generates questions that can be answered with provided text.
        Your task is to generate questions that can be answered with provided text.
        Questions should be separated with commas with no space. Your response shouldn't start and end with quotes. 
        Generate {question_count} questions for the given text.
        Text: {text}
        """
    ).strip()


def extract_keywords(text: str):
    return dedent(
        f"""
        SYSTEM INSTRUCTIONS:
        You are helpful assistant that extracts keywords from the given text.
        Your task is to extract keywords from the given text.
        Keywords should be separated with commas with no space. Your response shouldn't start and end with quotes.
        Example response with irrelevant keywords: science,birds,history,mathematics,flowers
        Text: {text}
        """
    ).strip()


def image_to_base64(image_path):
    """
    Convert an image file to base64 string
    """
    with Image.open(image_path) as image:
        # Convert image to bytes
        buffered = BytesIO()
        image.save(buffered, format=image.format)
        # Encode to base64
        img_str = base64.b64encode(buffered.getvalue())
        return img_str.decode('utf-8')


def save_base64_image(base64_string, output_path):
    """
    Convert a base64 string back to an image file
    """
    # Decode base64 string
    img_data = base64.b64decode(base64_string)
    # Create image from bytes
    img = Image.open(BytesIO(img_data))
    # Save image
    img.save(output_path + f".{img.format.lower()}")


def is_user_postgresql_quota_is_full(user_id: str, cursor: cursor):
    cursor.execute(sql.SQL("SELECT max_main_disk_size, main_disk_usage FROM user_quota WHERE user_id = %s;"), [
        user_id
    ])
    result = cursor.fetchone()

    return result[1] >= result[0] if True else False


def get_user_postgresql_usage_in_bytes(user_id: str, cursor: cursor):
    current_bytes = 0

    cursor.execute(sql.SQL(""""
    SELECT 
        pg_column_size(t.*) as row_size 
    FROM public.user t 
    WHERE id = %s;
    """), [user_id])

    current_bytes += cursor.fetchone()[0]


    return current_bytes
