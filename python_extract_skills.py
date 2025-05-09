import pandas as pd
import re
from datetime import datetime

# Load the CSV file with job descriptions
input_filename = "cwjobs_scraped_jobs_full_20250506_1331.csv"
df = pd.read_csv(input_filename)

# Print the column names to confirm
print("Available columns:", df.columns.tolist())

# Define a set of cybersecurity and technical skills to extract
skills_list = [
    # Cybersecurity-specific
    "SIEM", "SOC", "threat intelligence", "penetration testing", "vulnerability assessment",
    "incident response", "ISO 27001", "NIST", "risk assessment", "data protection", "GDPR",
    "security audit", "firewall", "IDS", "IPS", "DLP", "endpoint security", "identity management",
    "access control", "cyber essentials", "SOC analyst", "OWASP", "threat hunting", "zero trust",
    "CIS benchmarks", "network security", "cloud security",

    # General technical
    "Python", "Java", "C#", "JavaScript", "PowerShell", "Bash", "Linux", "Windows", "AWS", "Azure",
    "GCP", "Docker", "Kubernetes", "Terraform", "Ansible", "CI/CD", "DevOps", "Git", "Jenkins",
    "SQL", "NoSQL", "Splunk", "ELK", "LogRhythm", "Tenable", "Nessus", "Qualys", "Burp Suite",
    "Metasploit", "Wireshark"
]

# Create a regex pattern from the skill list
pattern = r'\b(?:' + '|'.join(re.escape(skill) for skill in skills_list) + r')\b'

# Skill extraction function
def extract_skills(description):
    if pd.isna(description):
        return ""
    found_skills = re.findall(pattern, description, flags=re.IGNORECASE)
    return ', '.join(sorted(set(skill.title() for skill in found_skills)))

# Apply the extraction
df["Extracted Skills"] = df["Description"].apply(extract_skills)

# Save to a new CSV with a timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
output_filename = f"cwjobs_skills_extracted_{timestamp}.csv"
df.to_csv(output_filename, index=False)

print(f"✅ Done! Saved extracted skills to {output_filename}")
