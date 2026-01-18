<div align="center">

# 🎯 Job Listing Scraper

### 🤖 Automated Indeed Job Search Tool

_Python script that scrapes job listings from multiple websites, extracts structured data, and outputs it in CSV format. Demonstrates web scraping, data processing, and automation with Python._


[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Contributing](#-contributing)

---

</div>

## ✨ Features

- 🖥️ **Interactive CLI** - User-friendly command-line interface for search customization
- 🔍 **Advanced Filtering** - Filter by job type, experience level, salary, and date posted
- 🧹 **Smart Data Processing** - Automatic deduplication and data validation
- 💰 **Salary Parsing** - Intelligently extracts and categorizes salary information (hourly vs yearly)
- 📊 **CSV Export** - Saves results with timestamps for easy tracking
- 📄 **Multiple Pages** - Scrapes multiple pages based on desired number of listings
- 🔌 **Extensible** - Easy to add scrapers for other job boards

## 🛠️ Technologies Used

- **Python 3.x** - Core programming language
- **Playwright** - Browser automation for dynamic content handling
- **BeautifulSoup4** - HTML parsing and data extraction
- **Pandas** - Data processing and CSV export
- **urllib** - URL encoding and parameter handling

## 📦 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/RichardOyelowo/Job-Scraper.git
cd Job-Scraper
```

2. **Create virtual environment (recommended):**

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers:**

```bash
playwright install chromium
```

## 🚀 Usage

Run the scraper:

```bash
python scraper.py
```

Follow the interactive prompts:

```
Enter job title (e.g., 'Python Developer', 'Software Engineer'): Python Developer
Enter location (e.g., 'Georgia', 'Atlanta, GA', 'Remote'): Georgia
Enter salary (e.g., '100000'): $80000
Jobs posted within last X days (1, 3, 7, 14 or press Enter for all): 7
Enter job type (e.g., 'Full', 'Part' 'Contract', 'Temporary', 'Internship'): full
Enter experience level (e.g., 'Mid', 'Entry', 'Senior'): entry
How many job listings do you want?(e.g. '10', '20'): 30

🔍 Starting scraper...
Scraping Jobs...
✅ Found 32 raw jobs

🧹 Processing data...
✅ After cleaning: 28 valid jobs

💾 Exporting to CSV...
✅ Saved to: output/jobs_20260112_143022.csv

🎉 Done! Check the output folder for your CSV file.
```

## 📋 Output Format

CSV file includes the following columns:

- `job_title` - Job position title
- `company` - Company name
- `location` - Job location
- `salary` - Original salary string
- `salary_min` - Parsed minimum salary
- `salary_max` - Parsed maximum salary
- `salary_type` - "yearly" or "hourly"
- `job_type` - Full-time, Part-time, Contract, etc.
- `description` - Brief job description snippet
- `url` - Direct link to job posting
- `scraped_at` - Timestamp of when data was collected

## 📁 Project Structure

```
Job-Scraper/
├── scrapers/
│   ├── __init__.py
│   └── indeed_scraper.py    # Indeed-specific scraping logic
├── output/                   # Generated CSV files
├── scraper.py               # Main entry point
├── config.py                # Configuration constants
├── data_processor.py        # Data cleaning and validation
├── exporter.py              # CSV export functionality
├── requirements.txt         # Python dependencies
├── .gitignore
└── README.md
```

## 🔧 Adding More Job Sites

To scrape additional job boards, create a new scraper file in the `scrapers/` directory:

1. **Create new scraper file** (e.g., `scrapers/linkedin_scraper.py`)

2. **Implement a class that returns the same dictionary structure:**

```python
class LinkedInScraper:
    def __init__(self, filters):
        self.filters = filters

    def scrape_multiple_pages(self, pages=5):
        # Your scraping logic here
        return html_pages

    def parse_job_card(self, html_pages):
        jobs = []
        # Parse HTML and return list of dicts with these keys:
        # job_title, company, location, salary, job_type,
        # description, url, scraped_at
        return jobs
```

3. **Use in `scraper.py`:**

```python
from scrapers.linkedin_scraper import LinkedInScraper

scraper = LinkedInScraper(filters)
html_pages = scraper.scrape_multiple_pages(pages=3)
jobs = scraper.parse_job_card(html_pages)
```

The data processor and exporter will work seamlessly with any scraper following this pattern.

## ⚠️ Known Limitations

### 🖥️ Browser Visibility Requirement

**The scraper runs in visible browser mode (`headless=False`) by default.** This is necessary because:

- Indeed uses Cloudflare Bot Management which blocks headless browsers
- Headless mode or non-standard viewports result in incomplete data or CAPTCHAs
- Running headful with a desktop viewport (1920x1080) ensures full data access

**Key constraint:**

```
✅ Headful + realistic viewport → full data loaded
❌ Headless or small viewport → blocked / partial data
```

**Users can modify line 37 in `scrapers/indeed_scraper.py`:**

```python
headless=True  # Try this if your IP isn't flagged
```

However, results may be limited if Indeed's anti-bot detection triggers.

### 🚦 Rate Limiting

- Indeed implements rate limiting and bot detection
- Excessive requests may result in temporary IP blocks
- Recommended to space out scraping sessions
- Consider using the scraper for personal job search, not mass data collection

### 📄 Pagination

- Each page returns approximately 10-15 jobs
- The scraper calculates pages based on desired listing count
- Some searches may have fewer results than requested

## 🚀 Future Improvements

- [ ] Add support for LinkedIn, Glassdoor, and other job boards
- [ ] Implement proxy rotation for better rate limit handling
- [ ] Add email notifications when new jobs matching criteria are found
- [ ] Create web dashboard for viewing and filtering results
- [ ] Add database storage option (SQLite/PostgreSQL)
- [ ] Implement job application tracking features
- [ ] Add API endpoints for programmatic access

## 💡 Use Case

Built to automate my own job search process during my transition into software development. This tool saves hours of manual searching by collecting and organizing job listings in one place, making it easier to track applications and identify opportunities.

## 🤝 Contributing

Contributions are welcome! If you'd like to add scrapers for other job sites or improve existing functionality:

1. Fork the repository
2. Create a feature branch
3. Ensure your scraper follows the standard dictionary format
4. Submit a pull request

## 📄 License

MIT License - feel free to use this project for your own job search!
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ⚖️ Disclaimer

This tool is for personal job search purposes only. Please respect Indeed's Terms of Service and robots.txt. Use responsibly and avoid excessive scraping that could impact their servers.

---

<div align="center">

**Built with love for development by [Richard](https://github.com/RichardOyelowo)**

_Currently seeking Software Developer opportunities in Python/Backend development_

📧 [Email](mailto:richard@richaffiliations.com) • 💼 [LinkedIn](https://www.linkedin.com/in/richard-oyelowo-b08410372/) • 🐙 [GitHub](https://github.com/RichardOyelowo)

</div>
