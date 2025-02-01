###    SCRAPING   ###
#####################
#Author : Alexandra Mitronika 2025
##################################


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re  # Import the regex library
import random

# Function to initialize and return a new browser instance
def init_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))



# [DATA APO PRWTES SELIDES]
TEXT1 = "https://www.skroutz.gr/c/40/kinhta-thlefwna.html"
TEXT2 = "?page="


# [ List to store data from all pages ]
all_phone_data = []

for i in range(2, 6):  # Iterate through pages
    driver = init_driver()
    TEXT3 = TEXT1 + TEXT2 + str(i)
    driver.get(TEXT3)

    try:
        while True:
            try:
                # Locate all card elements
                card_contents = driver.find_elements(By.CSS_SELECTOR, ".card-content")
                break  # Exit retry loop if successful
            except Exception as e:
                print("Error locating elements. Retrying...")
                time.sleep(1)

        phone_models = []
        phone_prices = []
        phone_rating = []
        phone_year = []

        # Extract model and price for each card
        for card in card_contents:
            try:
                model = card.find_element(By.TAG_NAME, "h2").text.strip()
                price = card.find_element(By.CSS_SELECTOR, "a.js-sku-link.sku-link").text.strip()
                rating = card.find_element(By.CSS_SELECTOR, '[data-testid="star-rating-value"]').text.strip()
                # Extract the year from the "specs" 
                specs = card.find_element(By.CSS_SELECTOR, "p.specs").get_attribute("title")
                #Search where Montelo with 4 digits
                year_match = re.search(r"Μοντέλο:\s*(\d{4})", specs)   
                year = year_match.group(1) if year_match else "Unknown"

                phone_models.append(model)
                phone_prices.append(price)
                phone_rating.append(rating)
                phone_year.append(year)
            except Exception as e:
                print(f"Error extracting data from a card: {e}")

        # Append the extracted data to our list
        for model, price, rating, year in zip(phone_models, phone_prices, phone_rating, phone_year):
            all_phone_data.append({"Phone Model": model, "Price": price, "Rating":rating, "Year":year})

    except Exception as e:
        print("Error extracting data from page:", e)

    finally:
        driver.quit()  # Close the driver for this page

# Put data in a dataframe using pandas
df = pd.DataFrame(all_phone_data)

# Clean and process the price in the df 
df["Price"] = df["Price"].replace({r'€': '', r'\.': '', r',': '.'}, regex=True).astype(float)

# Save data to CSV
df.to_csv("~/Desktop/cleaned_phone_data.csv", index=False, encoding="utf-8-sig")

print("Data from all pages collected and saved in a csv in your Desktop :)!!!")