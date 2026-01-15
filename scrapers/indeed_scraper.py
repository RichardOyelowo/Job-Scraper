from config import INDEED_BASE_URL, user_agent_generator
from playwright.sync_api import sync_playwright
from urllib.parse import urlencode
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import time


class IndeedScraper:

    def __init__(self, filters):
        self.filters = filters
        self.results_per_page = 10

    def build_url(self):
        return f"{INDEED_BASE_URL}?{urlencode(self.filters)}&vjk=8d8734a8fbc1a907"

    def scrape_page(self, page) -> str | None:
        """Scrape ONE page using browser navigation"""

        url = self.build_url()

        try:
            page.goto(url, wait_until="networkidle", timeout=5000)
            time.sleep(1)  # let CF finish scoring
            return page.content()
        except Exception as e:
            return None


    def scrape_multiple_pages(self, pages=5) -> list[str]:
        html_content = []

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )

            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                locale="en-US"
            )

            page = context.new_page()

            for count in range(pages):
                if count > 0:
                    self.filters["start"] = count * self.results_per_page

                html = self.scrape_page(page)
                if not html:
                    break

                html_content.append(html)

            browser.close()

        return html_content

    def parse_job_card(self, html_pages) -> list[dict]:
        """ loops through each card on the page and parses it """
        jobs = []

        for html in html_pages:
            soup = BeautifulSoup(html, "html.parser")
            full_item = soup.find_all("td", class_="resultContent")
            sub_item = soup.find_all("div", class_='slider_sub_item')

            for card,desc in zip(full_item, sub_item):
                title = card.select_one("h2.jobTitle a span")
                company = card.select_one("span[data-testid='company-name']")
                location = card.select_one("div[data-testid='text-location']")
                salary = card.select_one("div.css-1a6kja7 span.css-1pf4e7g")
                description = desc.select_one("div[data-testid='belowJobSnippet'] li")  # optional
                url_tag = card.select_one("h2.jobTitle a[href]")

                job_type_options = card.select("li.mosaic-provider-jobcards-ib5o0k")
                job_type = "".join(info.get_text(strip=True) for info in job_type_options) if job_type_options else None

                jobs.append({
                    "job_title": title.get_text(strip=True) if title else None,
                    "company": company.get_text(strip=True) if company else None,
                    "location": location.get_text(strip=True) if location else None,
                    "job_type": job_type,
                    "description": description.get_text(strip=True) if description else None,
                    "url": "https://www.indeed.com" + url_tag["href"] if url_tag else None,
                    "salary": salary.get_text(strip=True) if salary else None,                    
                    "scraped_at": datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
                })

        return jobs
