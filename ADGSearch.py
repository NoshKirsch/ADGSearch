#https://adg.org/api/member/search.json?location=413

# https://adg.org + url

import json
import time
import requests
from bs4 import BeautifulSoup

def parse_profile(url, headers):
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # --- Name ---
    name_el = soup.select_one(".MemberProfileInfoInner-infoName")
    name = name_el.get_text(strip=True) if name_el else None

    # --- Role ---
    role_el = soup.select_one(".MemberProfileInfoInner-infoJob")
    role = role_el.get_text(strip=True) if role_el else None

    # --- Email ---
    email = None
    email_link = soup.select_one('a[href^="mailto:"]')
    if email_link and email_link.has_attr("href"):
        email = email_link["href"].replace("mailto:", "").split("?")[0].strip()

    # --- Resume PDFs ---
    resumes = [
        a["href"].strip()
        for a in soup.select('.MemberProfileInfoInner-info-selfLinks a[href$=".pdf"]')
        if a.has_attr("href")
    ]
    # optional: take first resume if you only want one
    resume_link = resumes[0] if resumes else None

    # --- Credits ---
    credits = []
    credits_container = soup.select_one(".MemberProfileInfoInner-info-credits")
    if credits_container:
        for item in credits_container.find_all(recursive=False):
            text = item.get_text(" ", strip=True)
            if text:
                credits.append(text)

    return {
        "name": name,
        "role": role,
        "email": email,
        "resume": resume_link,   # first PDF resume
        "resumes": resumes,      # list of all PDF resumes
        "credits": credits
    }


url = "https://adg.org/api/member/search.json"
params = {"location": 413}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://adg.org/directory/"
}

response = requests.get(url, params=params, headers=headers)
response.raise_for_status()

# Parse manually (very robust)
members = json.loads(response.text)

BASE_URL = "https://adg.org"

profile_urls = [
    BASE_URL + member["url"]
    for member in members
    if "url" in member
]

print(profile_urls[:5])

resp = requests.get(profile_urls[0], headers=headers)

profiles = []

urlcounting = 0

for url in profile_urls:
    urlcounting += 1
    try:
        profile = parse_profile(url, headers)
        print("new parse")
        profiles.append(profile)
        time.sleep(1)
        print("count: " + str(urlcounting))
    except Exception as e:
        print(f"Failed {url}: {e}")


with open("adg_profiles.json", "w", encoding="utf-8") as f:
    json.dump(profiles, f, indent=2, ensure_ascii=False)



print(profiles)
