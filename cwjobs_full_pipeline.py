import csv
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure required nltk packages are available
nltk.download('punkt')
nltk.download('stopwords')

# Define known technical skills and certifications
technical_skills = [
    "python", "java", "c++", "c#", "javascript", "html", "css", "sql",
    "aws", "azure", "gcp", "linux", "docker", "kubernetes", "git",
    "bash", "powershell", "tcp/ip", "firewall", "encryption", "incident response",
    "network security", "vulnerability assessment", "penetration testing",
    "siem", "splunk", "burpsuite", "wireshark", "nmap"
]

certifications = [
    "ceh", "cissp", "cism", "security+", "oscp", "chfi", "ccsp",
    "gsec", "casp+", "cyber essentials", "iso 27001", "ccna", "crisc"
]

def extract_skills_and_certs(text):
    text = text.lower()
    words = word_tokenize(text)
    words = [w for w in words if w not in stopwords.words('english') and w.isalnum()]
    found_skills = sorted(set([w for w in words if w in technical_skills]))
    found_certs = sorted(set([w for w in words if w in certifications]))
    return ', '.join(found_skills), ', '.join(found_certs)

# Setup Chrome options for Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Launch browser
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.cwjobs.co.uk/jobs/cybersecurity/in-uk")

print("🔍 Waiting for job cards to load...")

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-title > a"))
    )
except:
    print("❌ Job cards not loaded — page may have failed. Message: ")
    driver.quit()
    print("📦 No jobs to save.")
    exit()

job_links = [a.get_attribute('href') for a in driver.find_elements(By.CSS_SELECTOR, ".job-title > a")]
print(f"🔗 Found {len(job_links)} job links")

results = []

for i, link in enumerate(job_links[:25], start=1):  # Limit to 25 jobs max
    try:
        driver.get(link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        title = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
        company = driver.find_element(By.CSS_SELECTOR, ".brand").text.strip()
        location = driver.find_element(By.CSS_SELECTOR, ".location").text.strip()
        description = driver.find_element(By.CSS_SELECTOR, ".job-description").text.strip()

        skills, certs = extract_skills_and_certs(description)

        results.append({
            "Job Title": title,
            "Company": company,
            "Location": location,
            "Job Link": link,
            "Description": description,
            "Technical Skills": skills,
            "Certifications": certs
        })

        print(f"✅ Scraped {i}: {title}")
    except Exception as e:
        print(f"⚠️ Error scraping job {i}: {e}")

driver.quit()

if results:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"cwjobs_combined_output_{timestamp}.csv"
    keys = results[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

    print(f"📁 Saved {len(results)} jobs to {filename}")
else:
    print("📦 No jobs to save.")
