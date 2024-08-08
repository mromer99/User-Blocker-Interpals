from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Replace with the path to your webdriver executable
geckodriver_path = '/usr/local/bin/geckodriver'

# Initialize the WebDriver for Firefox
driver = webdriver.Firefox(executable_path=geckodriver_path)

driver.maximize_window() # For maximizing window
driver.implicitly_wait(20) # gives an implicit wait for 20 seconds

# Navigate to the login page
driver.get('https://interpals.net/login.php')

# Wait for the consent pop-up and click the "Consent" button
try:
    consent_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'fc-cta-consent')]"))
    )
    consent_button.click()
except Exception as e:
    print(f"Consent button not found or an error occurred: {e}")

# Wait for the email input to be present and visible
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'topLoginEmail'))
)
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'topLoginEmail'))
)

# Replace 'your_email' with your actual email
email = driver.find_element(By.ID, 'topLoginEmail')
email.send_keys('your_email')

# Replace 'your_password' with your actual password
password = driver.find_element(By.ID, 'topLoginPassword')
password.send_keys('your_password')

# Find the login button and click it
login_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Sign In']")
login_button.click()

# Wait for the homepage to load completely by checking a unique element that appears only after login
try:
    home_page_loaded = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/pm.php')]"))
    )
except Exception as e:
    print(f"Homepage did not load or an error occurred: {e}")
    driver.quit()
    exit()

# Navigate to the messages page
try:
    messages_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/pm.php')]"))
    )
    messages_link.click()
except Exception as e:
    print(f"Messages link not found or an error occurred: {e}")

# Function to load older conversations
def load_older_conversations():
    while True:
        try:
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='load_more_conversations']"))
            )
            load_more_button.click()
            time.sleep(2)  # wait for the conversations to load
        except Exception as e:
            print("No more 'Load older conversations' button found or an error occurred.")
            break

# Function to check if the timestamp is within the range
def is_within_range(timestamp):
    match = re.match(r'(\d+)\s+(day|month)s?\s+ago', timestamp)
    if match:
        value, unit = int(match.group(1)), match.group(2)
        if unit == 'day':
            return 24 <= value <= 31
        elif unit == 'month':
            return 1 <= value <= 1
    return False

# Function to block user and delete conversation
def block_and_delete_conversation():
    # Wait for the messages to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tui_last_time')))

    # Find all messages within the desired time range
    messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'tui_last_time')]")
    print(f"Found {len(messages)} messages with timestamps.")

    # Filter messages based on the desired time range
    filtered_messages = [msg for msg in messages if is_within_range(msg.text)]
    print(f"Found {len(filtered_messages)} messages within the desired time range.")

    # Print account details before blocking
    accounts_to_block = []
    inactive_users = []

    for message in filtered_messages:
        try:
            timestamp = message.text
            parent_message = message.find_element(By.XPATH, "./ancestor::div[@class='th_wrap']")
            username_element = parent_message.find_element(By.XPATH, ".//div[contains(@class, 'tui_el') and (contains(@class, 'female') or contains(@class, 'male'))]")
            username = username_element.text.split(",")[0]
            
            if 'Inactive User' in username:
                inactive_users.append(f"Timestamp: {timestamp}, Username: Inactive User")
            elif message in filtered_messages:
                city = parent_message.find_element(By.XPATH, ".//div[contains(@class, 'tui_flag')]/following-sibling::div[contains(@class, 'tui_el')]").text
                age = parent_message.find_element(By.XPATH, ".//span[@class='tui_age']").text.strip(",")
                accounts_to_block.append(f"Timestamp: {timestamp}, Username: {username}, City: {city}, Age: {age}")

        except Exception as e:
            print(f"An error occurred while finding account details: {e}")

    # Print all accounts that will be blocked
    for account in accounts_to_block:
        print(account)

   

    # List all inactive users regardless of timestamp
    for message in messages:
        try:
            timestamp = message.text
            parent_message = message.find_element(By.XPATH, "./ancestor::div[@class='th_wrap']")
            username_element = parent_message.find_element(By.XPATH, ".//div[contains(@class, 'tui_el') and (contains(@class, 'female') or contains(@class, 'male'))]")
            username = username_element.text.split(",")[0]
            
            if 'Inactive User' in username and username not in [acc.split(",")[1].split(":")[1].strip() for acc in inactive_users]:
                inactive_users.append(f"Timestamp: {timestamp}, Username: Inactive User")
        except Exception as e:
            print(f"An error occurred while listing inactive accounts: {e}")

    # Print all inactive accounts regardless of timestamp
    print("All inactive accounts:")
    for inactive in inactive_users:
        print(inactive)


    # Block and delete accounts
    for message in filtered_messages:
        try:
            parent_message = message.find_element(By.XPATH, "./ancestor::div[@class='th_wrap']")
            delete_button = parent_message.find_element(By.XPATH, ".//i[contains(@class, 'fa-ban')]")
            delete_button.click()

            # Wait for the confirmation popup and confirm the action
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()

            time.sleep(1)  # wait for the action to complete

        except Exception as e:
            print(f"An error occurred: {e}")    
    
    

# Load older conversations before performing the block and delete actions
load_older_conversations()

# Call the function to perform the blocking and deletion
block_and_delete_conversation()

# Close the WebDriver
driver.quit()
