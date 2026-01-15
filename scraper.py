from scrapers.indeed_scraper import IndeedScraper
from data_processor import process_jobs
from exporter import export_to_csv
import pprint


def validate_required(prompt):
    """Get required input - keeps asking until provided"""
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("This field is required. Please enter a value.")


def validate_int(prompt):
    """Get optional integer input"""
    user_input = input(prompt).strip()
    if user_input:
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input, skipping this filter...")
            return None
    return None


# Build filters
filters = {}

# Required inputs
job_title = validate_required(
    "Enter job title (e.g., 'Python Developer', 'Software Engineer'): "
).strip()

location = validate_required(
    "Enter location (e.g., 'Georgia', 'Atlanta, GA', 'Remote'): "
)

filters["q"] = job_title
filters["l"] = location


#Optional filters
salary = validate_int("Enter salary (e.g., '100000'): $")
if salary:
    filters["salary"] = f"${salary}"

date_posted = validate_int(
    "Jobs posted within last X days (1, 3, 7, 14 or press Enter for all): "
)
if date_posted:
    filters["fromage"] = date_posted

# Job type
j_type = (
    input(
        "Enter job type (e.g., 'Full', 'Part' 'Contract', 'Temporary', 'Internship'): "
    ).strip().lower()
)
job_type = (
    "internship"
    if j_type == "internship"
    else (
        "temporary"
        if j_type == "temporary"
        else (
            "contract"
            if j_type == "contract"
            else f"{j_type}time" if j_type in ["full", "part"] else None
        )
    )
)
if job_type:
    filters["jt"] = job_type

# experience value
exp = input("Enter experience level (e.g., 'Mid', 'Entry', 'Senior'): ").strip().lower()
experience = f"{exp}_level" if exp in ["mid", "entry", "senior"] else None
if experience:
    filters["explvl"] = experience

# Handling Jobs count
listings = input("How many job listings do you want?(e.g. '10', '20'): ")

# TODO: Create scraper and run
scraper = IndeedScraper(filters)

print("\n🔍 Starting scraper...")
scraper = IndeedScraper(filters)

# Scrape
if listings and int(listings):
    pages = round(int(listings) / 10)
    html_pages = scraper.scrape_multiple_pages(pages)
else:
    html_pages = scraper.scrape_multiple_pages()
 

print("Scraping Jobs...")
raw_jobs = scraper.parse_job_card(html_pages)
print(f"✅ Found {len(raw_jobs)} raw jobs")

# Process
print("\n🧹 Processing data...")
cleaned_jobs = process_jobs(raw_jobs)

# Export
print("\n💾 Exporting to CSV...")
filepath = export_to_csv(cleaned_jobs)
print(f"✅ Saved to: {filepath}")

print("\n🎉 Done! Check the output folder for your CSV file.")
