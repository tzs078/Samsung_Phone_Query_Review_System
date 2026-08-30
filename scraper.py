import requests
from bs4 import BeautifulSoup
import json
import time

phones = {
    "Samsung Galaxy S21": "https://www.gsmarena.com/samsung_galaxy_s21_5g-10626.php",
    "Samsung Galaxy S22": "https://www.gsmarena.com/samsung_galaxy_s22-11253.php",
    "Samsung Galaxy S23": "https://www.gsmarena.com/samsung_galaxy_s23-12082.php",
    "Samsung Galaxy S24": "https://www.gsmarena.com/samsung_galaxy_s24-12773.php",
    "Samsung Galaxy S25": "https://www.gsmarena.com/samsung_galaxy_s25-13610.php",
    "Samsung Galaxy S21 Ultra": "https://www.gsmarena.com/samsung_galaxy_s21_ultra_5g-10596.php",
    "Samsung Galaxy S22 Ultra": "https://www.gsmarena.com/samsung_galaxy_s22_ultra_5g-11251.php",
    "Samsung Galaxy S23 Ultra": "https://www.gsmarena.com/samsung_galaxy_s23_ultra-12024.php",
    "Samsung Galaxy S24 Ultra": "https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php",
    "Samsung Galaxy S25 Ultra": "https://www.gsmarena.com/samsung_galaxy_s25_ultra-13322.php",
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_phones = []

for phone_name, url in phones.items():

    print(f"\nScraping: {phone_name}")

    try:
        response = requests.get(url, headers=headers, timeout=20)

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print("Failed:", phone_name)
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Get phone name from page
        title = soup.find("h1", class_="specs-phone-name-title")

        if title:
            actual_name = title.get_text(strip=True)
        else:
            actual_name = phone_name

        specs = {}

        # Get specifications
        for table in soup.find_all("table"):
            for row in table.find_all("tr"):

                cells = row.find_all(["td", "th"])

                if len(cells) >= 2:
                    key = cells[0].get_text(" ", strip=True)
                    value = cells[-1].get_text(" ", strip=True)

                    if key and value:
                        specs[key] = value

        phone_data = {
            "name": actual_name,
            "url": url,
            "specifications": specs
        }

        all_phones.append(phone_data)

        print(f"Collected: {len(specs)} specifications")

        # Small delay between requests
        time.sleep(2)

    except Exception as e:
        print(f"Error scraping {phone_name}: {e}")


# Save data to JSON
with open("samsung_phones.json", "w", encoding="utf-8") as file:
    json.dump(all_phones, file, indent=4, ensure_ascii=False)

print("\n================================")
print("Scraping Completed!")
print(f"Total phones collected: {len(all_phones)}")
print("Data saved to: samsung_phones.json")
print("================================")