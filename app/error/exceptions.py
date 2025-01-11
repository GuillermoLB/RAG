from .codes import Errors, Warnings


class RAGException(Exception):
    def __init__(self, error: Errors | Warnings, code: int):
        self.error = error
        self.code = code

    def __str__(self):
        return self.error


class UserException(RAGException):
    """
    All User related exceptions with specific error codes
    """
