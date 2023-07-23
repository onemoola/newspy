def test_to_publication(newsorg_article) -> None:
    actual = newsorg_article.to_publication()

    assert (
        actual.slug
        == "fortune-why-a-former-softbank-partner-is-tackling-midcareer-dropoff-for-working-mothers"
    )
