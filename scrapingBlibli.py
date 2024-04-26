from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

# URL Store from Blibli.com 
url = "https://www.blibli.com/p/iphone-15-pro/is--APF-70017-00310-00011?pickupPointCode=PP-3381860"

# Set up the webdriver with headless disabled for Blibli.com
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--use_subprocess")
options.add_argument('--disable-notifications')
options.headless = False
driver = webdriver.Chrome(options=options)

# Open the URL in the browser
driver.get(url)

# Get Product Name
product_name_element = driver.find_element(By.CSS_SELECTOR, ".product-name")
product_name = product_name_element.text.strip()

# Array Data
reviews_data = []

# Array Rating
rating_filters = [5, 4, 3, 2, 1]

# **Manual Click on "See All Reviews" Button** (Modify as needed)
print("Click the 'See All Reviews' button in the browser window manually and press Enter to proceed...")
input()  # Wait for user to click the button manually

# Locate the element containing the review list
review_list_element = driver.find_element(
    By.CSS_SELECTOR, ".review-modal__body--list")

# Iterate through filter
for rating_filter in rating_filters:
    # Check Path
    rating_filter_element = driver.find_element(
        By.XPATH, f"//input[@id='bluchip-{rating_filter}']")
    # Filter Click
    rating_filter_element.click()

    # Scrolling to get data until n-times
    scroll_trigger_count = 0
    while scroll_trigger_count < 5:
        time.sleep(2)

        scroll_trigger_count += 1

        print(scroll_trigger_count)

    # Extract data from all reviews
    review_elements = review_list_element.find_elements(
        By.CSS_SELECTOR, ".review-item")
    for review_element in review_elements:
        try:
            rating_element = review_element.find_element(
                By.CSS_SELECTOR, ".blu-rating")
            rating = len(rating_element.find_elements(
                By.CSS_SELECTOR, ".star")) if rating_element else "None"

            date_element = review_element.find_element(
                By.CSS_SELECTOR, ".date")
            date = date_element.text.strip() if date_element else "None"

            username_element = review_element.find_element(
                By.CSS_SELECTOR, ".profile .name")
            username = username_element.text.strip() if username_element else "None"

            review_text_element = review_element.find_element(
                By.CSS_SELECTOR, ".text")
            review_text = review_text_element.text.strip() if review_list_element else "None"

            variations_element = review_element.find_element(
                By.CSS_SELECTOR, ".review-item__variant")
            variations = variations_element.text.strip() if variations_element else "None"

            reviews_data.append({
                "Product Name": product_name,
                "Variations": variations,
                "Rating": rating,
                "Username": username,
                "Date": date,
                "Review": review_text,
            })

        except NoSuchElementException:
            print("Element not found. Skipping...")
            continue

# Close Driver
driver.quit()

# Convert to DataFrame
df = pd.DataFrame(reviews_data)

# Save DataFrame to CSV
df.to_csv("blibli_reviews_iphone_15_pro.csv", index=False, sep=";")

print("Reviews scraped successfully!")
