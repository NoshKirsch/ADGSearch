import json
import csv

# Load JSON
with open(r'C:\Users\Noah\Desktop\adg_profiles.json', "r", encoding="utf-8") as f:
    data = json.load(f)

# Write CSV
with open("adg_profiles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # Header row (keys)
    header = ["name", "role", "email", "resume", "credits"]
    writer.writerow(header)

    for profile in data:
        # Join list fields (like credits) into a single string
        credits_str = "; ".join(profile.get("credits", []))
        writer.writerow([
            profile.get("name"),
            profile.get("role"),
            profile.get("email"),
            profile.get("resume"),
            credits_str
        ])
