import feedparser

from newspy.rss.models import RssArticle


def main():
    feed = feedparser.parse(
        "https://www.businesslive.co.za/rss/?publication=bl&section=markets"
    )
    feeds = feed["entries"]
    for feed in feeds:
        print(RssArticle.parse_obj(feed))


if __name__ == "__main__":
    main()
