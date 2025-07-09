import os

from pydantic import BaseModel

class Configuration(BaseModel):
    port: int = 3434
    milvus_uri: str
    allowed_origins: str
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    auth_server_uri: str
    is_prod: bool
    images_folder: str

current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, 'conf.json')

with open(config_path, 'r') as file:
    json_file = file.read()

if json_file is None:
    raise ValueError("Missing 'conf.json' file. You can create new one by copying 'conf.example.json' to 'conf.json'")

conf = Configuration.model_validate_json(json_file)
