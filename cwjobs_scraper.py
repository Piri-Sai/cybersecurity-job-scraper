import time
import csv
import re
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc

# Set up undetected Chrome
options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
driver = uc.Chrome(options=options)

# CWJobs search URL
start_url = 'https://www.cwjobs.co.uk/jobs/cyber-security/in-united-kingdom'
driver.get(start_url)
time.sleep(5)

# Scrape job links
job_links = []
job_cards = driver.find_elements(By.CSS_SELECTOR, "div.res-vurnku a")
print(f"🔍 Found {len(job_cards)} job cards")

for card in job_cards:
    link = card.get_attribute("href")
    if link and "/job/" in link and link not in job_links:
        job_links.append(link)

print(f"🔗 Extracted {len(job_links)} unique job links")

# Timestamp for filenames
timestamp = datetime.now().strftime('%Y%m%d_%H%M')
filename = f'cwjobs_scraped_jobs_full_{timestamp}.csv'

# Scrape job data
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Job Title", "Company", "Location", "Description"])

    for link in job_links:
        driver.get(link)
        time.sleep(3)

        try:
            job_title = driver.find_element(By.CSS_SELECTOR, "h1.job-ad-display-s80d2f").text.strip()
        except NoSuchElementException:
            job_title = "N/A"

        try:
            company = driver.find_element(By.CSS_SELECTOR, "a[data-at='header-company-logo']").text.strip()
        except NoSuchElementException:
            company = "N/A"

        try:
            location = driver.find_element(By.CSS_SELECTOR, "span[data-at='job-item-location']").text.strip()
        except NoSuchElementException:
            location = "N/A"

        try:
            list_items = driver.find_elements(By.CSS_SELECTOR, "span.job-ad-display-1q6nkf6 li")
            skills = [li.text.strip() for li in list_items if li.text.strip()]
            description = "\n".join(skills)
        except NoSuchElementException:
            description = "N/A"

        writer.writerow([job_title, company, location, description])
        print(f"✅ Scraped: {job_title}")

driver.quit()

# ========================
# Skill extraction section
# ========================

print("\n🔍 Extracting skills...")

df = pd.read_csv(filename)

skills_list = [
    "SIEM", "SOC", "threat intelligence", "penetration testing", "vulnerability assessment",
    "incident response", "ISO 27001", "NIST", "risk assessment", "data protection", "GDPR",
    "security audit", "firewall", "IDS", "IPS", "DLP", "endpoint security", "identity management",
    "access control", "cyber essentials", "SOC analyst", "OWASP", "threat hunting", "zero trust",
    "CIS benchmarks", "network security", "cloud security",
    "Python", "Java", "C#", "JavaScript", "PowerShell", "Bash", "Linux", "Windows", "AWS", "Azure",
    "GCP", "Docker", "Kubernetes", "Terraform", "Ansible", "CI/CD", "DevOps", "Git", "Jenkins",
    "SQL", "NoSQL", "Splunk", "ELK", "LogRhythm", "Tenable", "Nessus", "Qualys", "Burp Suite",
    "Metasploit", "Wireshark"
]

pattern = r'\b(?:' + '|'.join(re.escape(skill) for skill in skills_list) + r')\b'

def extract_skills(description):
    if pd.isna(description):
        return ""
    found_skills = re.findall(pattern, description, flags=re.IGNORECASE)
    return ', '.join(sorted(set(skill.title() for skill in found_skills)))

df["Extracted Skills"] = df["Description"].apply(extract_skills)

output_filename = f"cwjobs_skills_extracted_{timestamp}.csv"
df.to_csv(output_filename, index=False)

print(f"\n✅ All done! Extracted skills saved to: {output_filename}")
