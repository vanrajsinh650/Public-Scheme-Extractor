import os
import re
from urllib.parse import urlparse
from datetime import datetime


def validate_url(url: str) -> bool:
    """Validate if URL is properly formatted."""
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


def generate_filename(title: str, url: str) -> str:
    """Generate output filename from article title or URL."""
    if title and title != 'article':
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = re.sub(r'\s+', '_', filename.strip())
        filename = filename[:50]
    else:
        parsed = urlparse(url)
        filename = parsed.path.split('/')[-1] or parsed.netloc
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)[:50]

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{filename}_{timestamp}.md"


def ensure_output_dir() -> str:
    """Create output directory if it doesn't exist."""
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def save_markdown(markdown: str, filename: str) -> str:
    """Save markdown content to file."""
    output_dir = ensure_output_dir()
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)

    return filepath
