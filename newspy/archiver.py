import asyncio
from typing import Optional, Dict, Any
from urllib.parse import urljoin, quote_plus # For URL manipulation if needed

from bs4 import BeautifulSoup

# Assuming HttpClient and HttpMethod are correctly importable from newspy.shared
# If not, this will need adjustment or a more basic aiohttp call.
from newspy.shared.http_client import HttpClient, HttpMethod


async def fetch_from_archivemd(original_url: str, http_client: HttpClient) -> Optional[Dict[str, Any]]:
    """
    Fetches the content of a given URL from archive.md and extracts title and main text.
    """
    # archive.md typically uses the original URL directly in the path,
    # or sometimes a snapshot ID. For simplicity, we'll try direct URL.
    # A more robust solution might involve checking for existing snapshots or submitting.
    # For now, let's assume we are fetching an already archived page.
    
    # Ensure the original_url doesn't have a scheme for simple concatenation with archive.md
    # This is a basic way to handle it; more robust parsing might be needed.
    if original_url.startswith("http://"):
        original_url_path = original_url[len("http://"):]
    elif original_url.startswith("https://"):
        original_url_path = original_url[len("https://"):]
    else:
        original_url_path = original_url

    # Construct the archive.md URL.
    # archive.md might also use specific snapshot IDs, but fetching by URL often works.
    # Example: https://archive.md/https://www.example.com
    archivemd_url = f"https://archive.md/{original_url_path}"

    print(f"Attempting to fetch from archive.md: {archivemd_url}")

    try:
        html_content = await http_client.send(
            method=HttpMethod.GET,
            url=archivemd_url
        )

        if not html_content or not isinstance(html_content, str):
            print(f"No content or non-string content received from {archivemd_url}")
            return {"original_url": original_url, "archive_url": archivemd_url, "status": "failed", "error": "No content received"}

        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract title
        extracted_title = None
        if soup.title and soup.title.string:
            extracted_title = soup.title.string.strip()
        
        # Fallback for title if page <title> is generic (e.g., "archive.md")
        if not extracted_title or "archive.md" in extracted_title.lower():
            h1_title = soup.find('h1')
            if h1_title:
                extracted_title = h1_title.get_text(separator=" ", strip=True)
            else: # Try another common title holder if h1 fails or is still too generic
                # This could be a specific div/span id/class if known
                pass


        # Extract main article text
        # Common selectors for archive sites or news articles. This is speculative.
        # archive.md often has a specific structure, sometimes using IDs like 'article', 'content', or 'text'.
        # A known good selector for archive.is / archive.md is 'div#TEXT', then getting paragraphs.
        # Another one for the main text container is often a div with id 'articleTake', or 'article'.
        
        article_text_parts = []
        article_div = soup.find('div', id='article') # Common on archive.md
        if not article_div:
            article_div = soup.find('article') # HTML5 <article> tag
        if not article_div:
            # A very generic fallback: find the largest text block.
            # This is more complex and less reliable. For now, stick to common selectors.
            # For archive.md, sometimes the content is in a div that looks like a snapshot container.
            # Let's try a known one: div with id 'TEXT'
            article_div = soup.find('div', id='TEXT')


        if article_div:
            # Get all paragraph texts, join them.
            # This removes formatting but gets the content.
            paragraphs = article_div.find_all('p')
            if paragraphs:
                for p in paragraphs:
                    article_text_parts.append(p.get_text(separator=" ", strip=True))
            else: # If no <p> tags, get all text from the div
                article_text_parts.append(article_div.get_text(separator=" ", strip=True))
            
            extracted_text = "\n\n".join(article_text_parts)
        else:
            extracted_text = "Main article text not found with current selectors."
            print(f"Main text container not found for {archivemd_url}")


        if not extracted_title:
            extracted_title = "Title not found"
            print(f"Title not found for {archivemd_url}")


        return {
            "original_url": original_url,
            "archive_url": archivemd_url,
            "title": extracted_title,
            "text": extracted_text,
            "status": "success"
        }

    except Exception as e:
        print(f"Error during fetching or parsing {archivemd_url}: {e}")
        return {"original_url": original_url, "archive_url": archivemd_url, "status": "failed", "error": str(e)}

if __name__ == '__main__':
    # Example Usage (requires running in an async context with HttpClient)
    async def test_archiver():
        # This http_client is for testing purposes.
        # In actual use, it should be passed from the calling code (e.g., from newspy.client)
        # or managed appropriately if archiver is part of a larger async flow.
        from newspy.shared.http_client import HttpClient # Re-import for standalone test context
        
        # A URL known to be on archive.md for testing (replace with a real one if needed)
        # Note: Live testing against archive.md might be slow or rate-limited.
        test_url = "https://www.bbc.com/news/world-us-canada-59430605" # Example URL
        
        # Ensure aiohttp is installed if running this test directly
        # pip install aiohttp beautifulsoup4
        
        async with HttpClient() as client: # HttpClient needs to be used in an async with block
            archived_content = await fetch_from_archivemd(test_url, client)
        
        if archived_content:
            print("\\n--- Archived Content ---")
            print(f"Status: {archived_content.get('status')}")
            if archived_content.get('status') == 'success':
                print(f"Original URL: {archived_content.get('original_url')}")
                print(f"Archive URL: {archived_content.get('archive_url')}")
                print(f"Title: {archived_content.get('title')}")
                print(f"Text sample: {archived_content.get('text', '')[:200]}...") # Print a sample
            else:
                print(f"Error: {archived_content.get('error')}")
        else:
            print("Failed to fetch or parse archived content.")

    # To run this test:
    # Ensure you are in the /app directory or newspy is in PYTHONPATH
    # python -m newspy.archiver
    # asyncio.run(test_archiver())
    pass # Default to pass to avoid execution when just creating file
    # To enable test, uncomment asyncio.run(test_archiver()) and run `python /app/newspy/archiver.py`
    # from the command line, ensuring aiohttp and beautifulsoup4 are installed.
    # Note: The test part is more for demonstration; direct execution might fail in the tool's env.
    # For the tool, the file creation is the main goal.
    # The example usage is commented out to prevent auto-execution issues.
    # To run it, one would typically do:
    # ```bash
    # python3 -c 'import asyncio; from newspy.archiver import test_archiver; asyncio.run(test_archiver())'
    # ```
    # (after installing deps and ensuring PYTHONPATH)

async def run_test():
    from newspy.shared.http_client import HttpClient
    test_url = "https://www.example.com" # A simple, likely archived URL
    # A more specific article URL might be better if example.com isn't interesting on archive.md
    # test_url = "https://www.theverge.com/2023/10/26/23933449/google-ai-search-images-videos-about-this-image"

    print(f"Running test with URL: {test_url}")
    async with HttpClient() as client:
        archived_content = await fetch_from_archivemd(test_url, client)
    
    if archived_content:
        print("\\n--- Test Archived Content ---")
        print(f"Status: {archived_content.get('status')}")
        if archived_content.get('status') == 'success':
            print(f"Original URL: {archived_content.get('original_url')}")
            print(f"Archive URL: {archived_content.get('archive_url')}")
            print(f"Title: {archived_content.get('title')}")
            # print(f"Text: {archived_content.get('text')}") # Full text can be long
            print(f"Text sample: {archived_content.get('text', '')[:500]}...")
        else:
            print(f"Error: {archived_content.get('error')}")
    else:
        print("Failed to fetch or parse archived content during test.")

if __name__ == '__main__':
    # This allows running `python -m newspy.archiver` for a quick test
    # Ensure aiohttp, beautifulsoup4 are installed.
    # And that `newspy` is in the python path (e.g. run from /app)
    
    # To prevent automatic execution in some environments, keep it commented out by default
    # or guard it more strictly. For now, for testing this module:
    # print("Executing archiver.py test run...")
    # asyncio.run(run_test())
    pass
