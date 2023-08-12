import gzip
import shutil
from pathlib import Path


def compress_csv_to_gzip(csv_format: Path, gzip_format: Path):
    with open(csv_format, "rb") as csv_file:
        with gzip.open(gzip_format, "wb") as gzip_file:
            shutil.copyfileobj(csv_file, gzip_file)


if __name__ == "__main__":
    compress_csv_to_gzip(Path("data/rss_sources.csv"), Path("data/rss_sources.csv.gz"))
