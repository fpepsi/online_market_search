import os
from dotenv import load_dotenv
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


load_dotenv()
market_user = os.getenv("USER_NAME")
market_pass = os.getenv("PASS")


def dismiss_popups(driver):
    """Detects and dismisses pop-ups during web scraping."""
    try:
        # Wait for the pop-up close button to appear (adjust selector as needed)
        modal_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "modal-content"))
        )
        close_button = modal_content.find_element(By.XPATH, './/*[contains(@class, "close") or contains(@class, "Close") or contains(@class, "onboarding__close-button") or @id="onboardingCloseButton"]')
        close_button.click()
        print("Pop-up dismissed!")
    except TimeoutException:
        print("No pop-up appeared within the timeout.")
    except NoSuchElementException:
        print("Close button not found in the modal.")
    except Exception as e:
        print(f"An error occurred while handling the pop-up: {e}")


# Function to initialize the browser
def initialize_browser():
    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking") 
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    }
    )
    return driver


def random_delay():
    time.sleep(random.uniform(1, 3))


# Main application function
def main():
    # Initialize the browser
    driver = initialize_browser()

    try:
        # Open a webpage
        try:
            driver.get("https://www.shaws.com")
            dismiss_popups(driver)
        # Continue with your scraping logic
        except Exception as e:
            print(f"An error occurred after trying to enter the site: {e}")
        random_delay()
        dismiss_popups(driver)

        # Click the login button
        print("Clicking the login button")
        login_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//a[@aria-label="Sign In / Up menu"]')))
        dismiss_popups(driver)
        login_button.click()
        random_delay()

        # Wait for the Sign In label inside the modal
        print("Waiting for the Sign In label")
        sign_in_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="signin-dropdown"]//button[@aria-label="Sign in"]'))
        )
        sign_in_button.click()
        random_delay()
        dismiss_popups(driver)

        # Enter the username
        print("Entering the username")
        username_field = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "enterUsername")))
        username_field.send_keys(market_user)
        random_delay()

        # Select the " sign-in with password"  option
        print("Selecting the password sign-in option")
        button_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()=" Sign in with password "]')))
        button_element.click()
        random_delay()

        # Enter the password
        print("Entering the password")
        password_field = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "password")))
        password_field.send_keys(market_pass)
        random_delay()

        # Select the " sign-in "  option
        print("pressing final 'sign-in' button")
        sign_in_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Sign in"][type="submit"]')
        sign_in_button.click()
        random_delay()

    except Exception as e:
        print(f"An error occurred when trying to navigate the site: {e}")

    finally:
        if 'driver' in locals():
            print("Debugging information:")
            print(f"URL: {driver.current_url}")
            print("Press any key to close the driver...")
            input()  # Wait for user input
            driver.quit()

# Entry point of the script
if __name__ == "__main__":
    main()
