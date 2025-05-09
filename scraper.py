import time
import re
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime

# Parameters
keyword = "cybersecurity"
location = "United Kingdom"
max_jobs = 20

# Certs and skill keywords
cert_keywords = ['CISSP', 'CEH', 'CompTIA', 'CISA', 'CISM', 'Security+', 'OSCP']
skill_keywords = ['Python', 'SIEM', 'Risk', 'Cloud', 'Azure', 'AWS', 'Linux', 'Firewall', 'Penetration', 'ISO 27001']

# Setup Chrome
options = uc.ChromeOptions()
options.headless = False
driver = uc.Chrome(options=options)

# Go to Indeed
driver.get("https://www.indeed.co.uk")
time.sleep(2)

# Enter job search
driver.find_element(By.ID, "text-input-what").send_keys(keyword)
driver.find_element(By.ID, "text-input-where").clear()
driver.find_element(By.ID, "text-input-where").send_keys(location)
driver.find_element(By.ID, "text-input-where").send_keys(Keys.RETURN)
time.sleep(3)

job_data = []
jobs_scraped = 0
page = 0

while jobs_scraped < max_jobs:
    page += 1
    print(f"\n🔄 Scraping Page {page}...")

    cards = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')
    for card in cards:
        if jobs_scraped >= max_jobs:
            break

        try:
            title = card.find_element(By.TAG_NAME, 'h2').text.strip()
            company = card.find_element(By.CLASS_NAME, 'company_location').text.strip().split('\n')[0]
            link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')

            # Open job in new tab
            driver.execute_script("window.open(arguments[0]);", link)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)

            desc = driver.find_element(By.CLASS_NAME, 'jobsearch-jobDescriptionText').text

            certs = [cert for cert in cert_keywords if cert.lower() in desc.lower()]
            skills = [skill for skill in skill_keywords if skill.lower() in desc.lower()]
            summary = desc[:300].replace('\n', ' ') + "..."

            # Salary (if shown)
            try:
                salary_elem = driver.find_element(By.XPATH, "//span[contains(@class, 'salary-snippet')]")
                salary = salary_elem.text.strip()
            except:
                salary = "Not specified"

            # Experience level
            exp_level = "Entry-level" if re.search(r'\b(entry\s*level|graduate)\b', desc, re.IGNORECASE) else \
                        "Mid-level" if re.search(r'\b(3\+?\s*years|mid\s*level|experienced)\b', desc, re.IGNORECASE) else \
                        "Senior-level" if re.search(r'\b(senior|lead|principal)\b', desc, re.IGNORECASE) else \
                        "Not specified"

            job_data.append({
                "Job Title": title,
                "Company": company,
                "Certifications": ", ".join(certs) if certs else "None",
                "Skills": ", ".join(skills) if skills else "None",
                "Salary": salary,
                "Experience Level": exp_level,
                "Summary": summary
            })

            jobs_scraped += 1
            print(f"✅ {title} | {company} | Certifications: {', '.join(certs) if certs else 'None'}")

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            print(f"❌ Error: {e}")
            driver.switch_to.window(driver.window_handles[0])
            continue

    try:
        next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next']")
        next_btn.click()
        time.sleep(3)
    except:
        print("⚠️ No more pages available.")
        break

driver.quit()

# Save as CSV
df = pd.DataFrame(job_data)
filename = f"indeed_cyber_jobs_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
df.to_csv(filename, index=False)
print(f"\n✅ Done! {jobs_scraped} jobs saved to {filename}")
