import time
import csv
import os
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

PASSWORD = os.getenv('PASSWORD')
EMAIL = os.getenv('EMAIL')
EXAMPLE_URL = os.getenv('URL')

# keep Chrome browser open after program finishes.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options= chrome_options) # pass chrome_options as a parameter.
driver.get(EXAMPLE_URL)

time.sleep(3)

login_link = driver.find_element(By.LINK_TEXT, "Log in")
login_link.click()

time.sleep(3)

email_link = driver.find_element(By.ID, "email")
email_link.send_keys(EMAIL)

password_link = driver.find_element(By.ID, "password")
password_link.send_keys(PASSWORD)

login = driver.find_element(By.ID, "create-account")
login.click()

time.sleep(3)

menu_link = driver.find_element(By.LINK_TEXT, "🔍 Search")
menu_link.click()

time.sleep(3)
# search for everything with "chicken"
menu_tab = driver.find_element(By.ID, "search-box")
menu_tab.send_keys("Chicken", Keys.ENTER)

time.sleep(3)

# Get total items count before loop
total_items = driver.find_elements(By.CLASS_NAME, "table_item_name")

# Write header only once before the loop
with open("nutritional_info.csv", "w", newline="") as file:
    fieldnames = ['Name', 'Serving', 'Calories', 'Protein']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

# loop for all the items in the first page
for i in range(len(total_items)):
    # Re-fetch fresh elements every iteration
    table_items = driver.find_elements(By.CLASS_NAME, "table_item_name")
    table_items[i].click()
    time.sleep(3)

    item_name = driver.find_element(By.ID, "food-name").text
    serving_size = driver.find_element(By.ID, "serving-size").text
    calories = driver.find_element(By.ID, "calories").text
    protein_cell = driver.find_element(By.XPATH, "//td[@class='left' and contains(.,'Protein')]").text
    protein_value = protein_cell.replace("Protein", "").strip()

    print(f"Name: {item_name}")
    print(f"Serving: {serving_size}")
    print(f"Calories: {calories}")
    print(f"Protein: {protein_value}")
    print("-" * 50)

    # Append each row to the CSV
    with open("nutritional_info.csv", "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({
            'Name': item_name,
            'Serving': serving_size,
            'Calories': calories,
            'Protein': protein_value
        })

    driver.back()
    time.sleep(3)


input("Press Enter to close the browser...")  # Keeps script alive and browser open until Enter pressed
driver.quit()