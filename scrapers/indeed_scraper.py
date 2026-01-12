from config import INDEED_BASE_URL
from playwright.sync_api import sync_playwright
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from datetime import datetime
import time


class IndeedScraper:

    def __init__(self, filters):
        self.filters = filters
        self.results_per_page = 10

    def build_url(self):
        return f"{INDEED_BASE_URL}?{urlencode(self.filters)}"

    def scrape_page(self, page):
        """ Scraps jobs on each page"""

        url = self.build_url()
        page.goto(url, timeout=10000)

        return page.content()

    def scrape_multiple_pages(self, pages=5) -> list[dict]:

        html_content = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-web-security"
            ])

            # Context with realistic settings to run headless screen
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                java_script_enabled=True,
                ignore_https_errors=True
            )

            page = browser.new_page()

            for count in range(pages):
                self.filters["start"] = count * self.results_per_page
                time.sleep(4)

                content = self.scrape_page(page)
                if not content:
                    break

                html_content.append(content)


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
                date_posted = card.select_one("span.date")  # optional
                url_tag = card.select_one("h2.jobTitle a[href]")

                job_type_options = card.select("li.mosaic-provider-jobcards-ib5o0k")
                job_type = "".join(info.get_text(strip=True) for info in job_type_options) if job_type_options else None

                jobs.append({
                    "job_title": title.get_text(strip=True) if title else None,
                    "company": company.get_text(strip=True) if company else None,
                    "location": location.get_text(strip=True) if location else None,
                    "salary": salary.get_text(strip=True) if salary else None,
                    "job_type": job_type,
                    "description": description.get_text(strip=True) if description else None,
                    "url": "https://www.indeed.com" + url_tag["href"] if url_tag else None,
                    "date_posted": date_posted.get_text(strip=True) if date_posted else None,
                    "scraped_at": datetime.now().isoformat()
                })

        return jobs