class NewspyHttpException(Exception):
    def __init__(
        self,
        status_code: int,
        msg: str,
        reason: str | None = None,
        headers: dict | None = None,
    ):
        self._status_code = status_code
        self._msg = msg
        self._reason = reason
        if headers is None:
            headers = {}
        self.headers = headers

    def __str__(self):
        return f"status code: {self._status_code}, message: {self._msg}, reason: {self._reason}"
