import sys
import argparse
from scraper import scrape_article
from utils import validate_url, generate_filename, save_markdown


def main():
    parser = argparse.ArgumentParser(
        description='Scrape article pages and convert to markdown format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py "https://example.com/article"
  python main.py "https://supportgowhere.life.gov.sg/schemes/kDqp5pnl/..."
        '''
    )

    parser.add_argument('url', help='Article URL to scrape')
    args = parser.parse_args()

    url = args.url.strip('"\'')

    if not validate_url(url):
        print(f"Error: Invalid URL format: {url}")
        sys.exit(1)

    print(f"Scraping: {url}")

    try:
        result = scrape_article(url)

        filename = generate_filename(result['title'], url)
        filepath = save_markdown(result['markdown'], filename)

        print(f"[OK] Success! Article saved to: {filepath}")
        print(f"  Title: {result['title']}")
        print(f"  Content length: {len(result['markdown'])} characters")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
