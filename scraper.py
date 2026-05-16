import requests
from bs4 import BeautifulSoup
import html2text
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright


def fetch_page(url: str) -> str:
    """Fetch HTML content from URL using Playwright for JavaScript support."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle')
            html = page.content()
            browser.close()
        return html
    except Exception as e:
        raise Exception(f"Failed to fetch {url}: {str(e)}")


def extract_content(html: str) -> str:
    """Extract main article content from HTML."""
    soup = BeautifulSoup(html, 'lxml')

    for tag in soup(['script', 'style', 'nav', 'footer']):
        tag.decompose()

    main_content = None

    for selector in ['article', 'main', '[role="main"]', '.content', '.post', '.entry', '[class*="content"]', '[class*="article"]']:
        if isinstance(selector, str) and selector.startswith('.'):
            main_content = soup.select_one(selector)
        elif isinstance(selector, str) and selector.startswith('['):
            main_content = soup.select_one(selector)
        else:
            main_content = soup.find(selector)
        if main_content:
            break

    if not main_content:
        main_content = soup.find('body') or soup

    return str(main_content)


def convert_to_markdown(html: str) -> str:
    """Convert HTML content to markdown format."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0

    markdown = h.handle(html)
    return markdown.strip()


def scrape_article(url: str) -> dict:
    """Main scraper function that combines all steps."""
    html = fetch_page(url)
    content = extract_content(html)
    markdown = convert_to_markdown(content)

    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('title')
    title_text = title.string if title else 'article'

    return {
        'title': title_text,
        'url': url,
        'markdown': markdown,
        'status': 'success'
    }
