def test_to_publication(article) -> None:
    actual = article.to_publication()

    assert (
        actual.slug
        == "fortune-why-a-former-softbank-partner-is-tackling-mid-career-drop-off-for-working-mothers"
    )
