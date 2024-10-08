import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

class TestTermsConditions():
    def setup_method(self, method):
        # Use headless Chrome for CI environments
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.vars = {}
    
    def teardown_method(self, method):
        self.driver.quit()
    
    def test_termsConditions(self):
        # Navigate to the homepage
        self.driver.get("https://smoothmaths.co.uk/")
        self.driver.set_window_size(1296, 696)

        # Scroll down to find the Terms & Conditions link in the footer
        self.driver.execute_script("window.scrollTo(0, 2770)")
        element = self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(3) > span")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        # Click on the Terms & Conditions link
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(3) > span").click()

        # Wait until the new page is loaded and get the current URL
        WebDriverWait(self.driver, 10).until(EC.url_contains("terms-conditions"))

        # Capture the current URL and assert that it matches the expected URL
        current_url = self.driver.current_url
        assert current_url == "https://smoothmaths.co.uk/terms-conditions/", f"Unexpected URL: {current_url}"

        # Take a screenshot
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = f"screenshots/terms_conditions_{timestamp}.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        self.driver.save_screenshot(screenshot_path)

