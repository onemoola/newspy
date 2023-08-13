import string
from datetime import datetime


def to_datetime(date_string: str) -> datetime:
    try:
        # Replace is added to support both 3.10 and 3.11
        # See: https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat
        transformed = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    except ValueError:
        try:
            transformed = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            try:
                transformed = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                try:
                    transformed = datetime.strptime(
                        date_string, "%a, %d %b %Y %H:%M:%S %z"
                    )
                except ValueError:
                    transformed = datetime.strptime(
                        date_string, "%a, %d %b %Y %H:%M:%S %Z"
                    )

    return transformed


def slugify(sentence: str) -> str:
    return (
        sentence.lower()
        .translate(str.maketrans("", "", string.punctuation))
        .replace(" ", "-")
    )
