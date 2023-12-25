import os
from typing import List
from bsup import download_html
import html2text
from requests_html import HTMLSession


def download_and_save_in_markdown(url: str, dir_path: str) -> None:
    """Download the HTML content from the web page and save it as a markdown file."""
    # Extract a filename from the URL
    if url.endswith("/"):
        url = url[:-1]

    filename = url.split("/")[-1] + ".md"
    print(f"Downloading {url} into {filename}...")

    session = HTMLSession()
    response = session.get(url, timeout=30)

    # Render the page, which will execute JavaScript
    response.html.render()

    # Convert the rendered HTML content to markdown
    h = html2text.HTML2Text()
    markdown_content = h.handle(response.html.raw_html.decode("utf-8"))

    # Write the markdown content to a file
    filename = os.path.join(dir_path, filename)
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)


def download(pages: List[str]) -> str:
    """Download the HTML content from the pages and save them as markdown files."""
    # Create the content/notion directory if it doesn't exist
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(base_dir, "content", "blogs")
    os.makedirs(dir_path, exist_ok=True)
    for page in pages:
        download_html(page, dir_path)
    return 


PAGES = [
    "https://www.clearquran.com/downloads/quran-english-translation-clearquran-edition-allah.pdf"
    ]

if __name__ == "__main__":
    download(PAGES)
