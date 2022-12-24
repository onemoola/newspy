from datetime import datetime


def to_datetime(string: str) -> datetime:
    try:
        # Replace is added to support both 3.10 and 3.11
        # See: https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat
        transformed = datetime.fromisoformat(string.replace("Z", "+00:00"))
    except ValueError:
        try:
            transformed = datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            transformed = datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%fZ")

    return transformed
