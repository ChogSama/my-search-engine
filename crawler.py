import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

visited = set()

def crawl(url, depth = 0, max_depth = 1000000000):
    """
    Crawls the given URL up to max_depth.
    Saves page text in ./data/
    """
    if depth > max_depth or url in visited:
        return

    print(f"[{depth}] Crawling: {url}")

    try:
        response = requests.get(url, timeout = 5)
        if 'text/html' not in response.headers.get('Content-Type', ''):
            print(f"Skipping non-HTML content: {url}")
            return
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return

    visited.add(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract text
    page_text = soup.get_text(separator = "\n").strip()
    print(f"Extracted text (first 200 chars): {page_text[:200]}")

    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok = True)

    # Save page test
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc.replace('.', '_').replace(':', '_')
    filename = f"data/{netloc}_{depth}.txt"
    print(f"Saving to file: {filename}")

    #Write text
    with open(filename, "w", encoding = "utf-8") as f:
        f.write(page_text)
    print(f"Wrote {len(page_text)} characters to {filename}")

    # Extract and follow links (only same domain)
    for link_tag in soup.find_all('a', href = True):
        next_url = urljoin(url, link_tag['href'])
        if urlparse(next_url).netloc == urlparse(url).netloc:
            crawl(next_url, depth + 1, max_depth)

if __name__ == "__main__":
    seed_url = "http://localhost:8000/test_site/page1.html"
    crawl(seed_url)