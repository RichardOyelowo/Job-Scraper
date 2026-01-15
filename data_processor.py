def remove_duplicates(jobs):

    seen_urls = set()
    deduplicated_jobs = []

    for item in jobs:
        url = item.get("url")
        if url and url not in seen_urls:
            seen_urls.add(item["url"])
            deduplicated_jobs.append(item)

    return deduplicated_jobs


def clean_salary_strings(salary_str):
    """returns a salary_type, min & max value for the salary strings"""

    value = {"salary_type": None, "salary_min": None, "salary_max": None}

    if not salary_str:
        return value

    text = (
        salary_str.replace(",", "").replace("to", "-").replace("$", "").replace(" ", "")
    )

    try:
        if "-" in text:
            parts = text.split("-")
            if len(parts) == 2:
                try:
                    value["salary_min"] = int(parts[0])
                    value["salary_max"] = int(parts[1])
                except ValueError:
                    return value
        else:
            try:
                value["salary_min"] = int(text)
                value["salary_max"] = int(text)
            except ValueError:
                return value

            if value["salary_min"] is not None:
                value["salary_type"] = (
                    "yearly" if value["salary_min"] > 1000 else "hourly"
                )

    except ValueError:
        pass

    return value


def validate_job(job):
    if not job.get("job_title"):
        return False

    if not job.get("company"):
        return False

    if not job.get("url"):
        return False

    return True


def process_jobs(jobs):
    """removes invalid jobs, clears & format jobs"""

    cleaned_jobs = remove_duplicates(jobs)

    processed_jobs = []

    for job in cleaned_jobs:
        if not validate_job(job):
            continue

        salary_infos = clean_salary_strings(job.get("salary"))

        job["salary_max"] = salary_infos["salary_max"]
        job["salary_min"] = salary_infos["salary_min"]
        job["salary_type"] = salary_infos["salary_type"]

        processed_jobs.append(job)

    return processed_jobs
