import datetime as dt
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from jose import jwt

from src.core.exceptions.auth_exceptions import InvalidTokenError
from src.core.settings import settings

ACCESS_TOKEN_EXP_TIME = timedelta(minutes=30)
REFRESH_TOKEN_EXP_TIME = timedelta(days=30)


def generate_access_token(user_id: UUID) -> str:
    """
    Generates a new access token for the given user ID.
    """
    now = datetime.utcnow()
    expiration_time = now + ACCESS_TOKEN_EXP_TIME
    payload = {"sub": str(user_id), "exp": expiration_time, "jit": str(uuid4())}
    token: str = jwt.encode(payload, settings.app_secret_key, algorithm="HS256")
    return token


def generate_refresh_token(user_id: UUID) -> str:
    """
    Generates a new refresh token for the given user ID.
    """
    now = datetime.utcnow()
    expiration_time = now + REFRESH_TOKEN_EXP_TIME
    payload = {"sub": str(user_id), "exp": expiration_time, "jit": str(uuid4())}
    token: str = jwt.encode(payload, settings.app_secret_key, algorithm="HS256")
    return token


class TokenEntity:
    """
    TokenEntity represents an access token and its associated refresh token.
    """

    def __init__(
        self,
        user_id: UUID,
        access_token: str | None = None,
        refresh_token: str | None = None,
        created_at: dt.datetime | None = None,
        expires_at: dt.datetime | None = None,
    ) -> None:
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expiration_time = ACCESS_TOKEN_EXP_TIME

        if not created_at:
            self.created_at = dt.datetime.utcnow()
        else:
            self.created_at = created_at

        if not expires_at:
            self.expires_at = self.created_at + self.expiration_time
        else:
            self.expires_at = expires_at

        if not access_token or not refresh_token:
            self._regenerate_tokens()
        else:
            self.access_token = access_token
            self.refresh_token = refresh_token

    def is_expired(self) -> bool:
        """
        Checks if the token has expired.
        """
        return dt.datetime.utcnow() > self.expires_at

    def refresh(self) -> None:
        """
        Refreshes the access token using the provided refresh token.
        """
        self.access_token = generate_access_token(self.user_id)

    def to_dict(self) -> dict[str, str]:
        """
        Returns a dictionary representation of the token.
        """
        if not self.access_token or not self.refresh_token:
            raise InvalidTokenError

        return {
            "user_id": str(self.user_id),
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at.isoformat(),
        }

    def _regenerate_tokens(self) -> None:
        """
        Generates new access and refresh tokens.
        """
        self.access_token = generate_access_token(self.user_id)
        self.refresh_token = generate_refresh_token(self.user_id)
        self.created_at = dt.datetime.utcnow()
        self.expires_at = self.created_at + self.expiration_time
