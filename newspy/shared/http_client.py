import json
import asyncio
from enum import Enum
from xml.etree import ElementTree

import aiohttp
from aiohttp_retry import RetryClient, ExponentialBackoff

from newspy.shared.exceptions import NewspyHttpException


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
        timeout: int = 5,
        status_forcelist: tuple = (429, 500, 502, 503, 504),
        retries: int = MAX_RETRIES,
        backoff_factor: float = 0.3,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        self._timeout = timeout
        self._status_forcelist = status_forcelist
        self._retries = retries
        self._backoff_factor = backoff_factor
        self._session = session

    async def __aenter__(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self._timeout)
            )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def send(
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

        retry_options = ExponentialBackoff(
            attempts=self._retries,
            factor=self._backoff_factor,
            statuses=self._status_forcelist,
        )
        retry_client = RetryClient(
            client_session=self._session, retry_options=retry_options
        )

        try:
            async with retry_client.request(
                method.value,
                url,
                headers=headers,
                params=params,
                **args,
            ) as response:
                response.raise_for_status()

                match headers["Content-Type"]:
                    case "application/json":
                        results = await response.json()
                    case "application/rss+xml":
                        content = await response.read()
                        results = parse_xml(data=content, source_url=url)
                    case "application/zip":
                        results = await response.read()
                    case _:
                        # Read bytes and decode to string for text-based content types
                        content_bytes = await response.read()
                        try:
                            results = content_bytes.decode('utf-8')
                        except UnicodeDecodeError:
                            # Fallback or error handling if not UTF-8
                            results = content_bytes.decode('latin-1') # Or some other fallback
        except aiohttp.ClientResponseError as http_error:
            try:
                # Attempt to parse JSON error response
                error_data = await http_error.response.json()
                msg = error_data.get("error", {}).get("message")
                reason = error_data.get("error", {}).get("reason")
            except (json.JSONDecodeError, aiohttp.ContentTypeError):
                msg = http_error.message
                reason = None

            raise NewspyHttpException(
                status_code=http_error.status,
                msg=f"{url}:\n {msg}",
                reason=reason,
                headers=http_error.headers,
            )
        except aiohttp.ClientError as client_error: # Catch other aiohttp client errors
            raise NewspyHttpException(
                status_code=500, # Generic server error for unexpected client issues
                msg=f"{url}:\n Client Error: {client_error}",
                reason=str(client_error)
            )
        except (TypeError, ValueError):
            results = None

        return results


def parse_xml(data: bytes, source_url: str) -> list[dict[str, str]] | None:
    try:
        root = ElementTree.fromstring(data)
        items = []
        for item in root.findall(".//item"):
            title = item.find("title").text.strip()
            description = item.find("description").text.strip()
            link = item.find("link").text.strip()
            pub_date = item.find("pubDate").text.strip()
            items.append(
                {
                    "source_url": source_url,
                    "title": title,
                    "description": description,
                    "url": link,
                    "published": pub_date,
                }
            )
        return items
    except (ElementTree.ParseError, AttributeError):
        # Handle XML parsing errors
        return None
