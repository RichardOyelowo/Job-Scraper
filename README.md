
## **Flowchart for Whimsical:**
```
Job Listing Scraper

Main Flow:
- Start
- Load Config → config.py (Indeed URL, headers, CSV columns)
- User Input → scraper.py (job title, location, filters)
- Validate Input → scraper.py (check non-empty job title and location)
- Build Search URL → scrapers/indeed_scraper.py (construct Indeed URL with query params)
- Send HTTP Request → scrapers/indeed_scraper.py (GET request with headers, retry logic)
- Parse HTML → scrapers/indeed_scraper.py (BeautifulSoup extract job cards)
- Extract Job Data → scrapers/indeed_scraper.py (loop through cards: title, company, location, salary, URL, date)
- Store Raw Data → scrapers/indeed_scraper.py (return list of job dictionaries)
- Clean Data → data_processor.py (remove duplicates, format salary, standardize dates)
- Validate Data → data_processor.py (ensure required fields present)
- Sort Data → data_processor.py (sort by date posted or relevance)
- Add Timestamp → exporter.py (add scraped_at column)
- Create CSV → exporter.py (pandas DataFrame to CSV)
- Save to Output → exporter.py (timestamped filename in output/)
- Display Summary → scraper.py (print total jobs found, search terms, filename)
- End

Error Handling:
- HTTP Request Failed → Retry (max 3 with 2s delay) → Log error if still fails
- Parse Error → Log which job failed → Skip that job → Continue
- No Jobs Found → Display message → Suggest adjusting search terms

User Input Flow:
- Job Title (required) → validate not empty
- Location (required) → validate not empty
- Salary filter (optional) → skip if empty
- Job Type (optional) → show menu or skip
- Experience Level (optional) → show menu or skip
- Date Posted (optional) → 1/3/7/14 days or skip

Files:
- scraper.py (main entry, user input, orchestration)
- config.py (constants, URLs, headers)
- scrapers/__init__.py (empty)
- scrapers/indeed_scraper.py (IndeedScraper class)
- data_processor.py (clean, validate, dedupe, sort)
- exporter.py (CSV export with timestamp)
- requirements.txt (requests, beautifulsoup4, pandas, lxml)
- .gitignore (venv/, output/*.csv, __pycache__/)
- README.md (documentation)
```
