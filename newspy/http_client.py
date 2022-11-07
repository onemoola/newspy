import json
from enum import Enum

import requests
import urllib3

from newspy.exceptions import NewspyException


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"


class HttpClient:
    MAX_RETRIES = 3
    DEFAULT_RETRY_CODES = (429, 500, 502, 503, 504)

    def __init__(
            self,
            requests_session: bool = True,
            requests_timeout: int = 5,
            status_forcelist: tuple = DEFAULT_RETRY_CODES,
            retries: int = MAX_RETRIES,
            status_retries: int = MAX_RETRIES,
            backoff_factor: float = 0.3,
    ) -> None:
        """
        :param requests_session:
            A Requests session object or a truthy value to create one.
            A falsy value disables sessions.
            It should generally be a good idea to keep sessions enabled
            for performance reasons (connection pooling).
        :param proxies:
            Definition of proxies (optional).
            See Requests doc https://2.python-requests.org/en/master/user/advanced/#proxies
        :param requests_timeout:
            Tell Requests to stop waiting for a response after a given
            number of seconds
        :param status_forcelist:
            Tell requests what type of status codes retries should occur on
        :param retries:
            Total number of retries to allow
        :param status_retries:
            Number of times to retry on bad status codes
        :param backoff_factor:
            A backoff factor to apply between attempts after the second try
            See urllib3 https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html
        """
        self._requests_timeout = requests_timeout
        self._status_forcelist = status_forcelist
        self._backoff_factor = backoff_factor
        self._retries = retries
        self._status_retries = status_retries

        if isinstance(requests_session, requests.Session):
            self._session = requests_session
        else:
            if requests_session:  # Build a new session.
                self._build_session()
            else:  # Use the Requests API module as a "session".
                self._session = requests.api

    def _build_session(self) -> None:
        self._session = requests.Session()
        retry = urllib3.Retry(
            total=self._retries,
            connect=None,
            read=False,
            allowed_methods=frozenset(["GET", "POST"]),
            status=self._status_retries,
            backoff_factor=self._backoff_factor,
            status_forcelist=self._status_forcelist,
        )

        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        self._session.mount("https://", adapter)

    def send(
            self,
            method: HttpMethod,
            url: str,
            headers: dict | None = None,
            params: dict | None = None,
            payload: dict | None = None,
    ) -> json:
        args = {}
        if headers is None:
            headers = {"Content-Type": "application/json"}

        if payload:
            if headers["Content-Type"] == "application/json":
                args["data"] = json.dumps(payload)
            else:
                args["data"] = str(payload)

        try:
            response = self._session.request(
                method,
                url,
                headers=headers,
                timeout=self._requests_timeout,
                params=params,
                **args,
            )

            response.raise_for_status()
            results = response.json()
        except requests.exceptions.HTTPError as http_error:
            response = http_error.response
            try:
                json_response = response.json()
                error = json_response.get("error", {})
                msg = error.get("message")
                reason = error.get("reason")
            except ValueError:
                msg = response.text or None
                reason = None

            raise NewspyException(
                status_code=response.status_code,
                msg="%s:\n %s" % (response.url, msg),
                reason=reason,
                headers=response.headers,
            )
        except requests.exceptions.RetryError as retry_error:
            request = retry_error.request
            try:
                reason = retry_error.args[0].reason
            except (AttributeError, IndexError):
                reason = None
            raise NewspyException(
                status_code=429,
                msg="%s:\n %s" % (request.path_url, "Max Retries"),
                reason=reason,
            )
        except (TypeError, ValueError):
            results = None

        return results
