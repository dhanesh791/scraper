import time
import json
import os
import wget
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc


def download_image(url):
    image_name = url.split("/")[-1]
    destination = "images/" + image_name
    if os.path.exists(destination):
        return True
    wget.download(url, destination)


def get_items(search, page, driver):
    search = search.replace(" ", "_")
    url = f"https://www.alibaba.com/products/{search}.html?IndexArea=product_en&page={page}"
    driver.get(url)

    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    items = driver.find_elements(By.CSS_SELECTOR, ".fy23-search-card")
    output = []

    for i in items:
        try:
            price = i.find_element(By.CSS_SELECTOR, ".search-card-e-price-main").text
        except:
            price = None

        try:
            name = i.find_element(By.CSS_SELECTOR, "h2").text
        except:
            name = None

        try:
            product_url = i.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
        except:
            product_url = None 

        try:
            MOQ = i.find_element(By.CSS_SELECTOR, ".search-card-m-sale-features__item.tow-line").text
        except:
            MOQ = None     

        try:
            product_image = i.find_element(By.CSS_SELECTOR, "search-card-e-slider__link search-card-e-slider__normal")
            product_image = "http:" + product_image if product_image else None
        except:
            product_image = None
            
        if product_image:
            try:
                download_image(product_image)
            except Exception as e:
                print(e)

        output.append({"name": name, "price": price, "MOQ":MOQ, "image": product_image, "url": product_url})

    return output


# Set up Selenium WebDriver
chrome_options = uc.options.ChromeOptions()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = uc.Chrome(options=chrome_options)

search = input("Enter Product to Search: ")
search_query = search.replace(" ", "_")

# Find max pages dynamically
driver.get(f"https://www.alibaba.com/products/{search_query}.html?IndexArea=product_en")
time.sleep(3)

max_page = 1
try:
    while max_page < 1:
        pagination_buttons = driver.find_elements(By.CSS_SELECTOR, ".searchx-pagination-list .pagination-item")
        if pagination_buttons:
            page_numbers = [int(btn.text) for btn in pagination_buttons if btn.text.isdigit()]
            if page_numbers:
                max_page = max(max_page, max(page_numbers))
                print(max_page)

        next_button = driver.find_element(By.CSS_SELECTOR, ".pagination-item.next")
        if next_button.get_attribute("disabled") is not None:
            break
        
        next_button.click()
        time.sleep(2)
except Exception as e:
    print("Pagination Error:", e)

driver.get(f"https://www.alibaba.com/products/{search_query}.html?IndexArea=product_en")
time.sleep(2)

print(f"Total pages found: {max_page}")

# Scrape all available pages
all_items = []
for page in range(1, max_page + 1):
    print(f"Scraping page {page}...")
    results = get_items(search, page, driver)
    all_items.extend(results)
    if not results:
        break

# Save the data to a JSON file
with open("product.json", "w") as f:
    json.dump(all_items, f, indent=2)

driver.quit()
print("Scraping completed. Data saved to product.json")

import pandas as pd

# Convert JSON to CSV
df = pd.DataFrame(all_items)
df.to_csv("product.csv", index=False, encoding="utf-8-sig")

print("Data also saved as product.csv")

