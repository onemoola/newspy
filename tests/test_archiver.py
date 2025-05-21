import pytest
from unittest.mock import AsyncMock, patch

from newspy.archiver import fetch_from_archivemd
from newspy.shared.http_client import HttpClient # Required for type hinting if passing mock
from newspy.shared.exceptions import NewspyHttpException # For simulating HTTP errors

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

SAMPLE_ARCHIVEMD_HTML_SIMPLE = """
<html>
<head><title>Test Article Title</title></head>
<body>
    <div id="TEXT">
        <h1>Another H1 Title, should be ignored if title tag is good</h1>
        <p>This is the first paragraph.</p>
        <p>This is the second paragraph with <a>a link</a>.</p>
    </div>
    <div id="article"> <!-- Alternative structure -->
        <p>Alternative paragraph 1</p>
    </div>
</body>
</html>
"""

SAMPLE_ARCHIVEMD_HTML_NO_TEXT_DIV = """
<html>
<head><title>Title No Text Div</title></head>
<body>
    <h1>Main Title Here</h1>
    <article>
        <p>Content from article tag.</p>
    </article>
</body>
</html>
"""

SAMPLE_ARCHIVEMD_HTML_GENERIC_TITLE = """
<html>
<head><title>archive.md</title></head>
<body>
    <div id="TEXT">
        <h1>Actual Article Title H1</h1>
        <p>Some content.</p>
    </div>
</body>
</html>
"""

SAMPLE_ARCHIVEMD_HTML_MALFORMED = """
<html>
<head><title>Malformed Test</title>
<body>
    <div>Oops, unclosed tags or other issues...
"""


@pytest.fixture
def mock_http_client():
    client = AsyncMock(spec=HttpClient)
    # Configure __aenter__ and __aexit__ if HttpClient is used as a context manager in archiver
    # For fetch_from_archivemd, it's passed as an argument, so direct method mocking is enough.
    return client

async def test_fetch_from_archivemd_success_simple(mock_http_client):
    mock_http_client.send.return_value = SAMPLE_ARCHIVEMD_HTML_SIMPLE
    original_url = "http://example.com/article1"
    
    result = await fetch_from_archivemd(original_url, mock_http_client)

    mock_http_client.send.assert_called_once()
    assert result is not None
    assert result["status"] == "success"
    assert result["original_url"] == original_url
    assert result["archive_url"] == "https://archive.md/example.com/article1"
    assert result["title"] == "Test Article Title"
    assert "This is the first paragraph." in result["text"]
    assert "This is the second paragraph with a link." in result["text"]
    assert "Alternative paragraph 1" not in result["text"] # Because #TEXT was found

async def test_fetch_from_archivemd_success_no_text_div(mock_http_client):
    mock_http_client.send.return_value = SAMPLE_ARCHIVEMD_HTML_NO_TEXT_DIV
    original_url = "http://example.com/article2"

    result = await fetch_from_archivemd(original_url, mock_http_client)
    
    assert result["status"] == "success"
    assert result["title"] == "Title No Text Div" # Should take from <title>
    assert "Content from article tag." in result["text"]

async def test_fetch_from_archivemd_success_generic_title_uses_h1(mock_http_client):
    mock_http_client.send.return_value = SAMPLE_ARCHIVEMD_HTML_GENERIC_TITLE
    original_url = "http://example.com/article3"

    result = await fetch_from_archivemd(original_url, mock_http_client)

    assert result["status"] == "success"
    assert result["title"] == "Actual Article Title H1" # Fallback to H1
    assert "Some content." in result["text"]

async def test_fetch_from_archivemd_http_error(mock_http_client):
    mock_http_client.send.side_effect = NewspyHttpException(status_code=404, msg="Not Found")
    original_url = "http://example.com/nonexistent"

    result = await fetch_from_archivemd(original_url, mock_http_client)

    assert result is not None
    assert result["status"] == "failed"
    assert result["original_url"] == original_url
    assert "NewspyHttpException" in result["error"] # Check if exception string is part of error

async def test_fetch_from_archivemd_no_content_returned(mock_http_client):
    mock_http_client.send.return_value = None # Simulate no content
    original_url = "http://example.com/empty"

    result = await fetch_from_archivemd(original_url, mock_http_client)

    assert result is not None
    assert result["status"] == "failed"
    assert result["error"] == "No content received"

async def test_fetch_from_archivemd_parsing_error(mock_http_client):
    # Technically, BeautifulSoup is quite robust, but if underlying parser fails or content is truly mangled
    # For this test, we'll assume if BS4 can't find key elements, it means "parsing" failed for our needs.
    # Let's simulate a case where no known selectors are found.
    mock_http_client.send.return_value = "<html><head><title>Only Title</title></head><body>Just some random text</body></html>"
    original_url = "http://example.com/noselectors"

    result = await fetch_from_archivemd(original_url, mock_http_client)

    assert result["status"] == "success" # HTTP call was success
    assert result["title"] == "Only Title"
    assert result["text"] == "Main article text not found with current selectors."

async def test_fetch_from_archivemd_url_handling_schemeless(mock_http_client):
    mock_http_client.send.return_value = SAMPLE_ARCHIVEMD_HTML_SIMPLE
    original_url = "example.com/article1" # Schemeless
    
    await fetch_from_archivemd(original_url, mock_http_client)
    
    # Check the URL passed to http_client.send
    args, kwargs = mock_http_client.send.call_args
    called_url = kwargs.get('url')
    assert called_url == "https://archive.md/example.com/article1"

async def test_fetch_from_archivemd_url_handling_https(mock_http_client):
    mock_http_client.send.return_value = SAMPLE_ARCHIVEMD_HTML_SIMPLE
    original_url = "https://example.com/article1" # HTTPS
    
    await fetch_from_archivemd(original_url, mock_http_client)
    
    args, kwargs = mock_http_client.send.call_args
    called_url = kwargs.get('url')
    assert called_url == "https://archive.md/example.com/article1"

async def test_fetch_from_archivemd_empty_html(mock_http_client):
    mock_http_client.send.return_value = "" # Empty string HTML
    original_url = "http://example.com/emptyhtml"

    result = await fetch_from_archivemd(original_url, mock_http_client)
    
    assert result is not None
    assert result["status"] == "failed"
    assert result["error"] == "No content received" # Or specific parsing error if BS4 handles it that way

async def test_fetch_from_archivemd_title_not_found(mock_http_client):
    mock_http_client.send.return_value = "<html><body><div id='TEXT'><p>text</p></div></body></html>"
    original_url = "http://example.com/notitle"

    result = await fetch_from_archivemd(original_url, mock_http_client)
    assert result["status"] == "success"
    assert result["title"] == "Title not found"
    assert result["text"] == "text"

# Example of how to run a specific test if needed for debugging:
# if __name__ == "__main__":
#     async def main():
#         client = AsyncMock(spec=HttpClient)
#         client.send.return_value = SAMPLE_ARCHIVEMD_HTML_SIMPLE
#         url = "http://example.com/article1"
#         data = await fetch_from_archivemd(url, client)
#         print(data)
#     asyncio.run(main())
