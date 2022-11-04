from datetime import datetime


def to_datetime(string: str) -> datetime:
    try:
        transformed = datetime.fromisoformat(string)
    except ValueError:
        try:
            transformed = datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            transformed = datetime.strptime(
                string.rpartition(".")[0], "%Y-%m-%dT%H:%M:%S"
            )

    return transformed
