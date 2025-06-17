from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: str
    username: str
    is_active: bool = True
    _is_authenticated: bool = True

    @property
    def is_authenticated(self) -> bool:
        """Return True if user is authenticated."""
        return self._is_authenticated

    @property
    def is_anonymous(self) -> bool:
        """Return False for real users."""
        return False

    def get_id(self) -> str:
        """Return string representation of user id."""
        return str(self.id)

