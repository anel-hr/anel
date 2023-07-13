from src.core.exceptions.base import ApplicationError


class AuthenticationError(ApplicationError):
    pass


class AccessTokenExpiredError(AuthenticationError):
    pass


class RefreshTokenExpiredError(AuthenticationError):
    pass


class EmailAlreadyExistsError(AuthenticationError):
    pass


class InvalidTokenError(AuthenticationError):
    pass


class InvalidCredentialsError(AuthenticationError):
    pass