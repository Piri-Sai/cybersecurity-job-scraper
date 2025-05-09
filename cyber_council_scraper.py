import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime

# Initialize ChromeDriver
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920x1080")

driver = uc.Chrome(options=options)

# UK Cyber Security Council Career Framework URL
council_url = "https://www.ukcybersecuritycouncil.org.uk/careers-and-learning/cyber-career-framework/"

# Store extracted data
specialisms, descriptions, job_roles, certifications = [], [], [], []

# ✅ STEP 1: Extract Specialism Names & Links
driver.get(council_url)
time.sleep(5)

specialism_blocks = driver.find_elements(By.CLASS_NAME, "specialism-item")

specialism_links = []
specialism_names = []

for block in specialism_blocks:
    try:
        name = block.find_element(By.XPATH, ".//div[@class='specialism-item-content']/p").text.strip()
        link = block.find_element(By.XPATH, ".//a[contains(text(), 'Learn more')]").get_attribute("href")
        specialism_links.append(link)
        specialism_names.append(name)
    except:
        continue  # Skip if not found

# ✅ STEP 2: Visit Each Specialism Page
for i, link in enumerate(specialism_links):
    driver.get(link)
    time.sleep(5)  # Let the page load
    
    print(f"🔍 Scraping: {specialism_names[i]}")

    # ✅ Extract Description
    try:
        description = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "hero-text"))
        ).text.strip()
    except:
        description = "N/A"

    # ✅ Extract Job Roles
    try:
        roles = [
            role.text.strip()
            for role in WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul li"))
            )
        ]
        roles_text = ", ".join(roles) if roles else "N/A"
    except:
        roles_text = "N/A"

    # ✅ Extract Certifications
    try:
        certs = [
            cert.text.strip()
            for cert in WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'credentialing')]"))
            )
        ]
        certs_text = ", ".join(certs) if certs else "N/A"
    except:
        certs_text = "N/A"

    print(f"✔ {specialism_names[i]} | {description} | Roles: {roles_text} | Certifications: {certs_text}\n")

    # ✅ Store data
    specialisms.append(specialism_names[i])
    descriptions.append(description)
    job_roles.append(roles_text)
    certifications.append(certs_text)

# ✅ STEP 3: Save Data to CSV
driver.quit()

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_path = f"C:/Users/piri/Documents/Final Year Project/cyber_career_framework_{timestamp}.csv"

df = pd.DataFrame({
    "Specialism": specialisms,
    "Description": descriptions,
    "Job Roles": job_roles,
    "Certifications": certifications
})

df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print(f"\n✅ Scraping completed! Data saved to {csv_path}")
