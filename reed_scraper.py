from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome options to make browser visible
options = Options()
options.add_argument("--start-maximized")  # You see the browser

# Launch browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Base URL
base_url = "https://www.reed.co.uk/jobs/cyber-security-jobs-in-united-kingdom"

# Lists to hold data
job_titles = []
companies = []
locations = []
certifications = []

# Loop over first 5 pages
for page in range(1, 6):
    print(f"🔄 Scraping Page {page}...")
    driver.get(f"{base_url}?pageno={page}")
    time.sleep(4)  # Let the page load

    job_cards = driver.find_elements(By.CLASS_NAME, "card")
    for card in job_cards:
        try:
            title = card.find_element(By.CLASS_NAME, "job-card_jobResultHeading__title__IQ8iT").text
        except:
            title = "N/A"

        try:
            company = card.find_element(By.CLASS_NAME, "job-card_jobResultHeading__postedBy__sK_25").text
        except:
            company = "N/A"

        try:
            location = card.find_element(By.CLASS_NAME, "job-card_jobMetadata__gJKG3").text
        except:
            location = "N/A"

        try:
            desc = card.find_element(By.CLASS_NAME, "job-card_jobResultDescription__Ga4A8").text.lower()
            cert = "Yes" if any(keyword in desc for keyword in ["certification", "certified", "ceh", "cissp", "comptia", "iso 27001"]) else "None"
        except:
            cert = "None"

        print(f"🔹 {title} | {company} | {location} | Certifications: {cert}")
        job_titles.append(title)
        companies.append(company)
        locations.append(location)
        certifications.append(cert)

# Done, close browser
driver.quit()

# Save results
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
df = pd.DataFrame({
    "Job Title": job_titles,
    "Company": companies,
    "Location": locations,
    "Certifications": certifications
})
output_file = f"reed_cyber_security_jobs_certified_{timestamp}.csv"
df.to_csv(output_file, index=False)

print(f"\n✅ Scraping complete. Saved to {output_file}")
