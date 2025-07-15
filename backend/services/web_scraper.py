import asyncio
import os
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
from typing import Optional, Tuple

class WebScraper:
    def __init__(self, output_dir="scraped_content"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    async def scrape_website(self, url: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove unwanted elements
                for element in soup(["script", "style", "nav", "footer", "header"]):
                    element.decompose()
                
                # Extract text content
                text = soup.get_text(separator='\n', strip=True)
                
                # Basic text cleaning
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                cleaned_text = '\n\n'.join(lines)
                
                return cleaned_text
        except httpx.RequestError as e:
            print(f"Request error for {url}: {str(e)}")
            return None
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None

    def save_to_markdown(self, content: str, url: str) -> Optional[str]:
        if not content:
            return None

        try:
            filename = url.replace('https://', '').replace('http://', '').replace('/', '_')
            filename = ''.join(c for c in filename if c.isalnum() or c in '-_.')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = os.path.join(self.output_dir, f"{filename[:30]}_{timestamp}.md")

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {url}\n\nScraped on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{content}")
            
            return filepath
        except Exception as e:
            print(f"Failed to save markdown: {str(e)}")
            return None

async def scrape_website_async(url: str) -> Optional[str]:
    scraper = WebScraper()
    try:
        content = await scraper.scrape_website(url)
        return scraper.save_to_markdown(content, url) if content else None
    except Exception as e:
        print(f"Scrape error: {str(e)}")
        return None

def scrape_website_sync(url: str) -> Optional[str]:
    return asyncio.run(scrape_website_async(url))