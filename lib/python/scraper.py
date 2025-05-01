import os
import csv
from playwright.sync_api import sync_playwright

URL = "https://climbodachi.com/climbing-gyms-directory/singapore/"

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)  # Make sure the directory exists

def scrape_table():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)

        # Wait for the table to load
        page.wait_for_selector("table#wpgmza_table_5 tbody tr")
        
        # Set up a list to store all data
        all_data = []
        
        # Loop through pages
        while True:
            # Extract rows from the current page
            rows = page.query_selector_all("table#wpgmza_table_5 tbody tr")
            for row in rows:
                cols = row.query_selector_all("td")
                all_data.append([col.inner_text().strip() for col in cols])
            
            # Check if the "Next" button is enabled, which indicates there are more pages
            next_button = page.query_selector("a#wpgmza_table_5_next")
            if "disabled" in next_button.get_attribute("class"):
                break  # No more pages, exit the loop
            
            # Click the "Next" button to go to the next page
            next_button.click()
            page.wait_for_timeout(1000)  # Wait a moment for the page to load

        browser.close()
        return all_data

def save_to_csv(data, filename="climbing_gyms.csv"):
    headers = ["Title", "Address", "Description", "Link"]
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

if __name__ == "__main__":
    gyms_data = scrape_table()
    save_to_csv(gyms_data)
    print(f"Saved {len(gyms_data)} rows to climbing_gyms.csv")
