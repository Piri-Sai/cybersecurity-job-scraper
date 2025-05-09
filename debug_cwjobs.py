from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
from datetime import datetime

# Setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Open CWJobs cyber security jobs
driver.get("https://www.cwjobs.co.uk/jobs/cyber-security")
time.sleep(5)

# Find job links using updated selector
job_cards = driver.find_elements(By.CSS_SELECTOR, ".search-result__title a")
print(f"🔍 Found {len(job_cards)} job cards")

jobs = []

for job in job_cards:
    title = job.text.strip()
    url = job.get_attribute("href")
    print(f"🔹 {title} | {url}")
    jobs.append({"title": title, "url": url})

# Save to CSV
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
filename = f"cwjobs_job_links_{timestamp}.csv"
with open(filename, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["title", "url"])
    writer.writeheader()
    writer.writerows(jobs)

print(f"\n✅ Done! Saved {len(jobs)} job links to {filename}")
driver.quit()
