import json
from enum import Enum

import requests
from requests.adapters import HTTPAdapter, Retry

from newspy.shared.exceptions import NewspyHttpException
from newspy.shared.xml_parser import parse_xml


class ContentType(str, Enum):
    JSON = "application/json"
    XML = "application/xml"


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"


class HttpClient:
    MAX_RETRIES = 3

    def __init__(
        self,
        requests_session: bool = True,
        requests_timeout: int = 5,
        status_forcelist: tuple = (429, 500, 502, 503, 504),
        retries: int = MAX_RETRIES,
        status_retries: int = MAX_RETRIES,
        backoff_factor: float = 0.3,
    ) -> None:
        """
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
        self._retries = retries
        self._status_retries = status_retries
        self._backoff_factor = backoff_factor

        if requests_session:  # Build a new session.
            self._build_session()
        else:  # Use the Requests API module as a "session".
            self._session = requests.api

    def _build_session(self) -> None:
        self._session = requests.Session()
        retry = Retry(
            total=self._retries,
            connect=1,
            read=False,
            allowed_methods=frozenset(["GET", "POST"]),
            status=self._status_retries,
            backoff_factor=self._backoff_factor,
            status_forcelist=self._status_forcelist,
        )

        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount("https://", adapter)

    def send(
        self,
        method: HttpMethod,
        url: str,
        headers: dict | None = None,
        params: dict | None = None,
        payload: dict | None = None,
    ) -> dict | list | bytes | str | None:
        args = {}
        results = None

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

            content_type = None
            if headers and "Content-Type" in headers:
                content_type = headers["Content-Type"]
            else:
                response_content_type = response.headers.get("Content-Type", "")
                if response_content_type:
                    content_type = response_content_type.split(";")[0].strip()

            match content_type:
                case "application/json":
                    results = response.json()
                case "application/rss+xml" | "application/xml" | "text/xml":
                    results = parse_xml(data=response.content, source_url=url)
                case "application/zip":
                    results = response.content
                case _:
                    try:
                        results = response.json()
                    except ValueError:
                        results = response.text

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

            raise NewspyHttpException(
                status_code=response.status_code,
                msg="%s:\n %s" % (response.url, msg),
                reason=reason,
                headers=response.headers,
            )
        except requests.exceptions.RetryError as retry_error:
            request = retry_error.request
            reason = retry_error.args[0].reason
            raise NewspyHttpException(
                status_code=429,
                msg="%s:\n %s" % (request.url, "Max Retries"),
                reason=reason,
            )
        except (TypeError, ValueError):
            results = None

        return results
