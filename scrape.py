from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver = webdriver.Chrome()

driver.get("https://www.scrapethissite.com/pages/ajax-javascript/")

wait = WebDriverWait(driver, 15)

data = []

years = ["2015", "2014", "2013", "2012", "2011", "2010"]

previous_title = ""

for year in years:

    print("Scraping year:", year)

    # Click the year
    year_button = wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, year)
        )
    )

    year_button.click()

    # Wait until the table has rows with actual data
    def data_loaded(driver):
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")

            if len(columns) >= 4:
                title = columns[0].text.strip()
                nominations = columns[1].text.strip()

                if title and nominations:
                    if title != previous_title:
                        return True

        return False

    wait.until(data_loaded)

    rows = driver.find_elements(
        By.CSS_SELECTOR,
        "table tbody tr"
    )

    print("Rows found:", len(rows))

    current_count = 0

    for row in rows:

        columns = row.find_elements(By.TAG_NAME, "td")

        if len(columns) < 4:
            continue

        title = columns[0].text.strip()
        nominations = columns[1].text.strip()
        awards = columns[2].text.strip()
        best_picture = columns[3].text.strip()

        # Skip incomplete rows
        if not title or not nominations or not awards:
            continue

        film_data = {
            "year": int(year),
            "title": title,
            "nominations": int(nominations),
            "awards": int(awards),
            "best_picture": best_picture
        }

        data.append(film_data)
        current_count += 1

    if current_count > 0:
        previous_title = data[-current_count]["title"]

    print("Films collected for", year + ":", current_count)
    print("Total films collected:", len(data))
    print("--------------------")


# Save all years
with open("oscars_all_years.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print("Data saved successfully!")
print("Total films:", len(data))

driver.quit()