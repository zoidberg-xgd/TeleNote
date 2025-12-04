"""PythonAnywhere Webapp Renewal Script

This script uses Selenium to automate clicking the "Run until 3 months from today" button
on PythonAnywhere's webapp configuration page.

PythonAnywhere does NOT provide an API for extending webapp expiry, so browser automation
is required.

Requirements:
    pip install selenium webdriver-manager

Environment Variables:
    PA_USERNAME: Your PythonAnywhere username
    PA_PASSWORD: Your PythonAnywhere password
    PA_DOMAIN: (Optional) Your webapp domain, defaults to {username}.pythonanywhere.com
"""
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False


def create_driver():
    """Create a headless Chrome WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    if USE_WEBDRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        driver = webdriver.Chrome(options=chrome_options)
    
    return driver


def renew_pythonanywhere():
    username = os.environ.get('PA_USERNAME')
    password = os.environ.get('PA_PASSWORD')
    
    if not username or not password:
        print("❌ Error: PA_USERNAME and PA_PASSWORD environment variables are required.")
        sys.exit(1)

    domain = os.environ.get('PA_DOMAIN', f'{username}.pythonanywhere.com')
    login_url = 'https://www.pythonanywhere.com/login/'
    # Convert domain to tab ID format: dots and hyphens become underscores, lowercase
    tab_id = domain.replace('.', '_').replace('-', '_').lower()
    webapp_url = f'https://www.pythonanywhere.com/user/{username}/webapps/#tab_id_{tab_id}'

    print(f"🚀 Starting renewal process for user: '{username}'")
    print(f"🎯 Target webapp: '{domain}'")
    print(f"📍 Webapp URL: {webapp_url}")

    driver = None
    try:
        print("1️⃣  Initializing headless Chrome browser...")
        driver = create_driver()
        wait = WebDriverWait(driver, 20)
        
        # 1. Navigate to login page
        print(f"2️⃣  Navigating to login page: {login_url}")
        driver.get(login_url)
        time.sleep(2)
        
        # 2. Fill in login form
        print("3️⃣  Filling in login credentials...")
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "id_auth-username"))
        )
        username_field.clear()
        username_field.send_keys(username)
        
        password_field = driver.find_element(By.ID, "id_auth-password")
        password_field.clear()
        password_field.send_keys(password)
        
        # 3. Submit login form
        print("4️⃣  Submitting login form...")
        login_button = driver.find_element(By.ID, "id_next")
        login_button.click()
        
        # Wait for login to complete
        time.sleep(3)
        
        # Check if login was successful
        if "login" in driver.current_url.lower():
            print("❌ Login failed. Please check your credentials.")
            print(f"   Current URL: {driver.current_url}")
            sys.exit(1)
        
        print("✅ Login successful!")
        
        # 4. Navigate to webapp configuration page
        print(f"5️⃣  Navigating to webapp page: {webapp_url}")
        driver.get(webapp_url)
        time.sleep(3)
        
        # 5. Find and click the "Run until 3 months from today" button
        print("6️⃣  Looking for 'Run until 3 months from today' button...")
        
        # Try multiple selectors to find the button
        button = None
        selectors = [
            # Button with specific text
            "//button[contains(text(), 'Run until 3 months')]",
            "//input[@type='submit' and contains(@value, 'Run until 3 months')]",
            # Form with extend action
            "//form[contains(@action, '/extend')]//button",
            "//form[contains(@action, '/extend')]//input[@type='submit']",
            # Class-based selectors
            "//button[contains(@class, 'extend')]",
            ".//button[contains(@class, 'btn') and contains(text(), 'Run')]",
        ]
        
        for selector in selectors:
            try:
                button = driver.find_element(By.XPATH, selector)
                if button and button.is_displayed():
                    print(f"   ✅ Found button with selector: {selector}")
                    break
            except NoSuchElementException:
                continue
        
        if not button:
            # Try CSS selector as fallback
            try:
                button = driver.find_element(
                    By.CSS_SELECTOR, 
                    "form[action*='extend'] button, form[action*='extend'] input[type='submit']"
                )
            except NoSuchElementException:
                pass
        
        if not button:
            print("❌ Could not find the extend button.")
            print("   📄 Page source preview:")
            print(driver.page_source[:2000])
            # Save screenshot for debugging
            driver.save_screenshot("debug_screenshot.png")
            print("   📸 Saved screenshot to debug_screenshot.png")
            sys.exit(1)
        
        # 6. Click the button
        print("7️⃣  Clicking the extend button...")
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(1)
        button.click()
        
        # Wait for the action to complete
        time.sleep(3)
        
        # 7. Verify success
        print("8️⃣  Verifying extension...")
        driver.refresh()
        time.sleep(2)
        
        # Check for new expiry date in page
        page_text = driver.page_source
        if "will be disabled on" in page_text:
            # Extract the new date
            import re
            date_match = re.search(r'will be disabled on\s+<strong>([^<]+)</strong>', page_text)
            if date_match:
                new_date = date_match.group(1)
                print(f"✅ Successfully extended!")
                print(f"   🎉 New expiry date: {new_date}")
            else:
                print("✅ Extension request completed!")
        else:
            print("✅ Extension request completed!")
            print("   ⚠️  Could not verify new expiry date from page.")
        
    except TimeoutException as e:
        print(f"❌ Timeout waiting for page element: {e}")
        if driver:
            driver.save_screenshot("timeout_screenshot.png")
            print("   📸 Saved screenshot to timeout_screenshot.png")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during renewal: {e}")
        if driver:
            driver.save_screenshot("error_screenshot.png")
            print("   📸 Saved screenshot to error_screenshot.png")
        sys.exit(1)
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed.")


if __name__ == "__main__":
    renew_pythonanywhere()
