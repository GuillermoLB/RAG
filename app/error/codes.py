class ErrorsWithCodes(type):
    def __getattribute__(self, code):
        msg = super().__getattribute__(code)
        if code.startswith("__"):  # python system attributes like __class__
            return msg
        else:
            return f"[{code}] {msg}"


class Warnings(metaclass=ErrorsWithCodes):
    pass


class Errors(metaclass=ErrorsWithCodes):
    E001 = "User not found"
