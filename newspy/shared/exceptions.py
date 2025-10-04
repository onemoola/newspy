from requests.structures import CaseInsensitiveDict


class NewspyException(Exception):

    def __init__(self, msg: str, reason: str | None = None) -> None:
        self.msg = msg
        self.reason = reason

    def __str__(self) -> str:
        return f"message: {self.msg}, reason: {self.reason}"


class NewspyHttpException(NewspyException):

    def __init__(
        self,
        status_code: int,
        msg: str,
        reason: str | None = None,
        headers: CaseInsensitiveDict[str] | None = None,
    ) -> None:
        super().__init__(msg, reason)
        self.status_code = status_code
        if headers is None:
            headers = CaseInsensitiveDict()
        self.headers = headers

    def __str__(self) -> str:
        return f"status code: {self.status_code}, message: {self.msg}, reason: {self.reason}"
