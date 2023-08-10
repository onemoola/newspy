from newspy import client


def test_configure_without_newsorg_api_key() -> None:
    client.configure()
    actual = client.default_client_config.get("newsorg_api_key")

    assert actual is None


def test_configure_with_newsorg_api_key() -> None:
    client.configure(newsorg_api_key="test")
    actual = client.default_client_config.get("newsorg_api_key")

    assert actual == "test"
