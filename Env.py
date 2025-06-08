import os
import dotenv
from enum import Enum
from typing import Dict, Any, TypeVar, Generic


# Define your environment variables as an Enum
class EnvKey(Enum):
    MILVUS_URI = "MILVUS_URI"
    PORT = "PORT"
    # Add other environment variables here

required_env_vars = [
    EnvKey.MILVUS_URI,
    EnvKey.PORT
]

T = TypeVar('T')

dotenv.load_dotenv()


class EnvMeta(type):
    _variables: Dict[EnvKey, Any] = {}
    _initialized = False

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if not cls._initialized:
            cls._init_once()
            cls._initialized = True

    def _init_once(cls):
        """Initialization that should happen only once"""
        # Check all required environment variables
        missing_vars = []
        for var in required_env_vars:
            if not os.environ.get(var.value):
                missing_vars.append(var.value)

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        # Pre-load required variables into _variables
        for var in required_env_vars:
            cls._variables[var] = os.environ.get(var.value)

    def __call__(cls, key: EnvKey) -> str:
        """
        Get environment variable value
        Args:
            key: EnvKey enum member
        Returns:
            str: Environment variable value
        Raises:
            ValueError: If environment variable is not found
        """
        if key not in cls._variables:
            env_value = os.environ.get(key.value)
            if env_value is None:
                raise ValueError(f"Missing required environment variable: {key.value}")
            cls._variables[key] = env_value

        return cls._variables[key]


class Env(metaclass=EnvMeta):
    pass