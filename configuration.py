from pydantic import BaseModel

class Configuaration(BaseModel):
    port: int = 3434
    aipool_ws_uri: str
    milvus_uri: str
    allowed_origins: str
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

# Replace 'file_path.json' with your actual JSON file path
if not 'conf.json' in __file__:
    raise ValueError("Missing 'conf.json' file. You can create new one by copying 'conf.example.json' to 'conf.json'")

with open('conf.json', 'r') as file:
    json_file = file.read()

conf = Configuaration.model_validate_json(json_file)
