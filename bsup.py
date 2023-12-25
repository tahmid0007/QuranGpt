from bs4 import BeautifulSoup
from bs4.element import Comment
import requests, re, os


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body.text, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    cleaned_text = u" ".join(t.strip() for t in visible_texts)
    cleaned_text = re.sub(' +', ' ', cleaned_text)  # Replace multiple spaces with a single space
    return cleaned_text.strip()


def download_html(url: str, dir_path: str):
    html = requests.get(url)
    text = text_from_html(html)

    filename = url.split("/")[-2] + ".md"
    filename = os.path.join(dir_path, filename)
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
