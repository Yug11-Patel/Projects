import json
import time

import psycopg2

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# =========================================================
# SETTINGS
# =========================================================

MAX_RESTAURANTS = 182

LISTING_URL = "https://www.zomato.com/ahmedabad/restaurants"


# =========================================================
# CREATE SELENIUM DRIVER
# =========================================================

def create_driver():

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    return driver


# =========================================================
# CONNECT TO POSTGRESQL
# =========================================================

def create_database_connection():

    connection = psycopg2.connect(
        host="localhost",
        database="zomato_db",
        user="postgres",
        password="yug",
        port="5432"
    )

    print("PostgreSQL connected successfully!")

    return connection


# =========================================================
# CREATE TABLE
# =========================================================

def create_table(connection):

    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS restaurants (

        id SERIAL PRIMARY KEY,

        url TEXT,
        name TEXT,
        rating TEXT,
        review_count TEXT,
        dining_rating TEXT,
        delivery_rating TEXT,
        cuisines TEXT,
        address TEXT,
        status TEXT,
        opening_time TEXT,
        cost_for_two TEXT,
        phone TEXT,

        menu_url TEXT,
        booking_url TEXT,
        direction_url TEXT,

        offers TEXT,

        digital_payments BOOLEAN,
        home_delivery BOOLEAN,
        takeaway BOOLEAN,
        parking BOOLEAN,
        stags_allowed BOOLEAN,
        luxury_dining BOOLEAN,
        indoor_seating BOOLEAN,
        family_friendly BOOLEAN,
        kid_friendly BOOLEAN,
        work_friendly BOOLEAN,
        free_parking BOOLEAN
    )
    """

    cursor.execute(query)

    cursor.execute("""
        ALTER TABLE restaurants
        ADD COLUMN IF NOT EXISTS offers TEXT
    """)

    connection.commit()

    cursor.close()

    print("Restaurants table is ready!")


# =========================================================
# GET RESTAURANT URLS
# =========================================================

def get_restaurant_urls(driver):

    driver.get(LISTING_URL)

    time.sleep(5)

    restaurant_urls = []

    previous_height = 0
    unchanged_count = 0

    while True:

        links = driver.find_elements(
            By.TAG_NAME,
            "a"
        )

        for link in links:

            try:

                href = link.get_attribute("href")

                if (
                    href
                    and "/info" in href
                    and "zomato.com/ahmedabad/" in href
                ):

                    # Remove query parameters
                    clean_url = href.split("?")[0]

                    if clean_url not in restaurant_urls:

                        restaurant_urls.append(clean_url)

            except Exception:

                continue

        print(
            "Restaurant URLs found so far:",
            len(restaurant_urls)
        )

        # Scroll down
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        time.sleep(3)

        current_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        if current_height == previous_height:

            unchanged_count += 1

        else:

            unchanged_count = 0

        previous_height = current_height

        # Stop after page height remains unchanged
        # for 3 consecutive checks
        if unchanged_count >= 3:

            break

    return restaurant_urls


# =========================================================
# CHECK WHETHER URL ALREADY EXISTS
# =========================================================

def restaurant_exists(connection, url):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM restaurants
        WHERE url = %s
        LIMIT 1
        """,
        (url,)
    )

    result = cursor.fetchone()

    cursor.close()

    if result:

        return True

    return False


# =========================================================
# SCRAPE RESTAURANT DETAILS
# =========================================================

def scrape_restaurant_details(driver, url):

    driver.get(url)

    time.sleep(3)

    # -----------------------------------------------------
    # GET PAGE TEXT
    # -----------------------------------------------------

    body_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text

    lines = []

    for line in body_text.splitlines():

        line = line.strip()

        if line:

            lines.append(line)

    # -----------------------------------------------------
    # DEFAULT VALUES
    # -----------------------------------------------------

    name = ""
    rating = ""
    review_count = ""
    dining_rating = ""
    delivery_rating = ""
    cuisines = ""
    address = ""
    status = ""
    opening_time = ""
    cost_for_two = ""
    phone = ""

    menu_url = ""
    booking_url = ""
    direction_url = ""

    offers = ""

    # -----------------------------------------------------
    # NAME
    # -----------------------------------------------------

    try:

        name = driver.find_element(
            By.XPATH,
            "//h1"
        ).text.strip()

    except Exception:

        pass

    # -----------------------------------------------------
    # RATING
    # -----------------------------------------------------

    for line in lines:

        if line in [
            "4.0",
            "4.1",
            "4.2",
            "4.3",
            "4.4",
            "4.5",
            "4.6",
            "4.7",
            "4.8",
            "4.9",
            "5.0"
        ]:

            rating = line

            break

    # -----------------------------------------------------
    # REVIEW COUNT
    # -----------------------------------------------------

    for line in lines:

        if "Reviews" in line:

            parts = line.split()

            for part in parts:

                if part.isdigit():

                    review_count = part

                    break

            if review_count:

                break

    # -----------------------------------------------------
    # DINING RATING
    # -----------------------------------------------------

    for i, line in enumerate(lines):

        if line == "Dining Ratings":

            if i + 1 < len(lines):

                dining_rating = lines[i + 1]

            break

    # -----------------------------------------------------
    # DELIVERY RATING
    # -----------------------------------------------------

    for i, line in enumerate(lines):

        if line == "Delivery Ratings":

            if i + 1 < len(lines):

                delivery_rating = lines[i + 1]

            break

    # -----------------------------------------------------
    # CUISINES
    # -----------------------------------------------------

    cuisine_names = [
        "Chinese",
        "Asian",
        "Indian",
        "North Indian",
        "South Indian",
        "Gujarati",
        "Italian",
        "Continental",
        "Mexican",
        "Thai",
        "Japanese",
        "Fast Food",
        "Cafe",
        "Desserts",
        "Beverages",
        "Mughlai",
        "Punjabi",
        "Street Food",
        "Biryani",
        "Pizza",
        "Bakery",
        "Seafood",
        "Lebanese",
        "Korean"
    ]

    found_cuisines = []

    try:

        cuisine_index = lines.index("Cuisines")

        for line in lines[
            cuisine_index + 1:
            cuisine_index + 10
        ]:

            if line in cuisine_names:

                if line not in found_cuisines:

                    found_cuisines.append(line)

    except ValueError:

        pass

    cuisines = ", ".join(found_cuisines)

    # -----------------------------------------------------
    # ADDRESS
    # -----------------------------------------------------

    for line in lines:

        if (
            "Ahmedabad" in line
            and len(line) > 25
            and "Restaurants" not in line
        ):

            address = line

            break

    # -----------------------------------------------------
    # COST FOR TWO
    # -----------------------------------------------------

    for line in lines:

        if "for two" in line.lower():

            cost_for_two = line

            break

    # -----------------------------------------------------
    # PHONE
    # -----------------------------------------------------

    for line in lines:

        if line.startswith("+91"):

            phone = line

            break

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    for line in lines:

        if line == "Closed":

            status = "Closed"

            break

        if line == "Open":

            status = "Open"

            break

    # -----------------------------------------------------
    # OPENING TIME
    # -----------------------------------------------------

    for line in lines:

        if line.startswith("Opens at"):

            opening_time = line

            break

    # -----------------------------------------------------
    # MENU URL
    # -----------------------------------------------------

    try:

        menu_links = driver.find_elements(
            By.XPATH,
            "//a[contains(@href, '/menu')]"
        )

        for link in menu_links:

            href = link.get_attribute("href")

            if href:

                menu_url = href

                break

    except Exception:

        pass

    # -----------------------------------------------------
    # BOOKING URL
    # -----------------------------------------------------

    try:

        booking_links = driver.find_elements(
            By.XPATH,
            "//a[contains(@href, '/book')]"
        )

        for link in booking_links:

            href = link.get_attribute("href")

            if href:

                booking_url = href

                break

    except Exception:

        pass

    # -----------------------------------------------------
    # DIRECTION URL
    # -----------------------------------------------------

    try:

        direction_links = driver.find_elements(
            By.XPATH,
            "//a[contains(@href, 'google.com/maps/dir')]"
        )

        for link in direction_links:

            href = link.get_attribute("href")

            if href:

                direction_url = href

                break

    except Exception:

        pass

    # -----------------------------------------------------
    # OFFERS
    # -----------------------------------------------------

    offer_keywords = [
        "PRE-BOOK OFFER",
        "INSTANT OFFER",
        "SURPRISE",
        "EXCLUSIVE OFFER",
        "BANK OFFER",
        "Flat",
        "OFF",
        "scratch card"
    ]

    found_offers = []

    offer_section = False

    for line in lines:

        if line == "Dining Offers":

            offer_section = True

            continue

        if offer_section:

            if line in [
                "Menu",
                "Cuisines",
                "Average Cost",
                "More Info"
            ]:

                break

            if any(
                keyword.lower() in line.lower()
                for keyword in offer_keywords
            ):

                if line not in found_offers:

                    found_offers.append(line)

    offers = " | ".join(found_offers)

    # -----------------------------------------------------
    # FACILITIES
    # -----------------------------------------------------

    page_lower = body_text.lower()

    digital_payments = (
        "digital payments accepted"
        in page_lower
    )

    home_delivery = (
        "home delivery"
        in page_lower
    )

    takeaway = (
        "takeaway available"
        in page_lower
    )

    parking = (
        "parking available"
        in page_lower
    )

    stags_allowed = (
        "stags allowed"
        in page_lower
    )

    luxury_dining = (
        "luxury dining"
        in page_lower
    )

    indoor_seating = (
        "indoor seating"
        in page_lower
    )

    family_friendly = (
        "family friendly"
        in page_lower
    )

    kid_friendly = (
        "kid friendly"
        in page_lower
    )

    work_friendly = (
        "work friendly"
        in page_lower
    )

    free_parking = (
        "free parking"
        in page_lower
    )

    # -----------------------------------------------------
    # CREATE DATA
    # -----------------------------------------------------

    data = {

        "url": url,
        "name": name,
        "rating": rating,
        "review_count": review_count,
        "dining_rating": dining_rating,
        "delivery_rating": delivery_rating,
        "cuisines": cuisines,
        "address": address,
        "status": status,
        "opening_time": opening_time,
        "cost_for_two": cost_for_two,
        "phone": phone,

        "menu_url": menu_url,
        "booking_url": booking_url,
        "direction_url": direction_url,

        "offers": offers,

        "digital_payments": digital_payments,
        "home_delivery": home_delivery,
        "takeaway": takeaway,
        "parking": parking,
        "stags_allowed": stags_allowed,
        "luxury_dining": luxury_dining,
        "indoor_seating": indoor_seating,
        "family_friendly": family_friendly,
        "kid_friendly": kid_friendly,
        "work_friendly": work_friendly,
        "free_parking": free_parking
    }

    return data


# =========================================================
# INSERT NEW RESTAURANT
# =========================================================

def insert_restaurant(connection, data):

    cursor = connection.cursor()

    columns = [
        "url",
        "name",
        "rating",
        "review_count",
        "dining_rating",
        "delivery_rating",
        "cuisines",
        "address",
        "status",
        "opening_time",
        "cost_for_two",
        "phone",
        "menu_url",
        "booking_url",
        "direction_url",
        "offers",
        "digital_payments",
        "home_delivery",
        "takeaway",
        "parking",
        "stags_allowed",
        "luxury_dining",
        "indoor_seating",
        "family_friendly",
        "kid_friendly",
        "work_friendly",
        "free_parking"
    ]

    values = tuple(
        data[column]
        for column in columns
    )

    placeholders = ", ".join(
        ["%s"] * len(columns)
    )

    column_names = ", ".join(columns)

    query = f"""
        INSERT INTO restaurants
        ({column_names})
        VALUES
        ({placeholders})
    """

    try:

        cursor.execute(
            query,
            values
        )

        connection.commit()

        print("Saved to PostgreSQL!")

        return True

    except Exception as error:

        connection.rollback()

        print(
            "PostgreSQL insert error:",
            error
        )

        return False

    finally:

        cursor.close()


# =========================================================
# SAVE JSON
# =========================================================

def save_json(data):

    with open(
        "restaurants.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nData saved to restaurants.json")


# =========================================================
# MAIN
# =========================================================

def main():

    connection = None
    driver = None

    all_restaurants = []

    try:

        # -------------------------------------------------
        # DATABASE
        # -------------------------------------------------

        connection = create_database_connection()

        create_table(connection)

        # -------------------------------------------------
        # SELENIUM
        # -------------------------------------------------

        driver = create_driver()

        # -------------------------------------------------
        # GET RESTAURANT URLS
        # -------------------------------------------------

        restaurant_urls = get_restaurant_urls(
            driver
        )

        print(
            "\nTotal restaurant URLs found:",
            len(restaurant_urls)
        )

        # -------------------------------------------------
        # KEEP ONLY FIRST 182
        # -------------------------------------------------

        restaurant_urls = restaurant_urls[
            :MAX_RESTAURANTS
        ]

        print(
            "Maximum restaurants to keep:",
            MAX_RESTAURANTS
        )

        print(
            "URLs being considered:",
            len(restaurant_urls)
        )

        # -------------------------------------------------
        # CHECK EXISTING DATA
        # -------------------------------------------------

        existing_count = 0
        missing_urls = []

        for url in restaurant_urls:

            if restaurant_exists(
                connection,
                url
            ):

                existing_count += 1

            else:

                missing_urls.append(url)

        print(
            "\nAlready saved in PostgreSQL:",
            existing_count
        )

        print(
            "Restaurants still missing:",
            len(missing_urls)
        )

        # -------------------------------------------------
        # IF ALL 182 ARE ALREADY SAVED
        # -------------------------------------------------

        if not missing_urls:

            print(
                "\nAll first 182 restaurants "
                "are already saved."
            )

            print(
                "Nothing will be scraped again."
            )

            return

        # -------------------------------------------------
        # SCRAPE ONLY MISSING RESTAURANTS
        # -------------------------------------------------

        for index, url in enumerate(
            missing_urls,
            start=1
        ):

            print(
                f"\nScraping missing restaurant "
                f"{index} of {len(missing_urls)}"
            )

            print(url)

            try:

                # Extra safety check
                if restaurant_exists(
                    connection,
                    url
                ):

                    print(
                        "Already exists. Skipping."
                    )

                    continue

                data = scrape_restaurant_details(
                    driver,
                    url
                )

                print(
                    "Name:",
                    data["name"]
                )

                print(
                    "Rating:",
                    data["rating"]
                )

                print(
                    "Reviews:",
                    data["review_count"]
                )

                print(
                    "Cuisines:",
                    data["cuisines"]
                )

                print(
                    "Address:",
                    data["address"]
                )

                print(
                    "Cost:",
                    data["cost_for_two"]
                )

                print(
                    "Phone:",
                    data["phone"]
                )

                print(
                    "Offers:",
                    data["offers"]
                )

                # -----------------------------------------
                # SAVE TO DATABASE
                # -----------------------------------------

                saved = insert_restaurant(
                    connection,
                    data
                )

                if saved:

                    all_restaurants.append(data)

            except Exception as error:

                print(
                    "Error scraping restaurant:",
                    error
                )

                continue

        # -------------------------------------------------
        # SAVE ONLY NEWLY SCRAPED DATA TO JSON
        # -------------------------------------------------

        if all_restaurants:

            save_json(
                all_restaurants
            )

        print(
            "\nNew restaurants scraped:",
            len(all_restaurants)
        )

        print(
            "Existing restaurants kept:",
            existing_count
        )

        print(
            "Maximum restaurant limit:",
            MAX_RESTAURANTS
        )

    except Exception as error:

        print(
            "\nERROR:",
            error
        )

    finally:

        if driver:

            driver.quit()

        if connection:

            connection.close()

        print(
            "\nConnections closed."
        )


# =========================================================
# RUN PROGRAM
# =========================================================

if __name__ == "__main__":

    main()