import feedparser

from newspy.rss.models import Article


def main():
    feed = feedparser.parse(
        "https://www.businesslive.co.za/rss/?publication=bl&section=markets"
    )
    feeds = feed["entries"]
    for feed in feeds:
        print(Article.parse_obj(feed))


if __name__ == "__main__":
    main()
