def test_to_article(newsorg_article) -> None:
    actual = newsorg_article.to_article()

    assert (
        actual.slug
        == "fortune-why-a-former-softbank-partner-is-tackling-midcareer-dropoff-for-working-mothers"
    )
