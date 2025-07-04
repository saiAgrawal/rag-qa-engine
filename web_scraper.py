import asyncio
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, output_dir="scraped_content"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    async def scrape_website(self, url):
        # Try BeautifulSoup fallback (Playwright/crawl4ai removed for now)
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.content, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            return soup.get_text()
        except Exception as e:
            print("Fallback scraper error:", e)
            return None

    def save_to_markdown(self, content, url):
        if not content:
            return None

        filename = url.replace('https://', '').replace('http://', '').replace('/', '_')
        filename = ''.join(c for c in filename if c.isalnum() or c in '-_.')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(self.output_dir, f"{filename[:30]}_{timestamp}.md")

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {url}\n\n{content}")
            return filepath
        except Exception as e:
            print("Failed to save markdown:", e)
            return None

def scrape_website_sync(url):
    scraper = WebScraper()
    try:
        content = asyncio.run(scraper.scrape_website(url))
        return scraper.save_to_markdown(content, url) if content else None
    except Exception as e:
        print("Scrape error:", e)
        return None
