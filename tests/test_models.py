def test_to_publication(newsapi_article) -> None:
    actual = newsapi_article.to_publication()

    assert (
        actual.slug
        == "fortune-why-a-former-softbank-partner-is-tackling-mid-career-drop-off-for-working-mothers"
    )
