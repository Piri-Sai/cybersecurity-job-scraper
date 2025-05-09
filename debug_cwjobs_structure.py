from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import time

# Set up the browser
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(), options=options)

# Go to CWJobs search results page
url = "https://www.cwjobs.co.uk/jobs/cyber-security"
driver.get(url)
time.sleep(5)  # Wait for page to load

# Find job cards (let’s print total tags that look like job containers)
cards = driver.find_elements(By.TAG_NAME, "article")
print(f"🕵️ Total <article> tags found: {len(cards)}")

# Let’s print their class names to understand the structure
for i, card in enumerate(cards[:10]):
    print(f"Card {i+1} class: {card.get_attribute('class')}")

driver.quit()
