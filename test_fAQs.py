import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

class TestFAQs():
    def setup_method(self, method):
        # Setup headless mode for CI environments
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.vars = {}

    def teardown_method(self, method):
        # Quit the driver after test execution
        self.driver.quit()

    def test_fAQs(self):
        # Navigate to the homepage
        self.driver.get("https://smoothmaths.co.uk/")
        self.driver.set_window_size(1296, 696)

        # Scroll down to the FAQ link in the footer and click it
        self.driver.execute_script("window.scrollTo(0, 4370.66650390625)")
        self.driver.find_element(By.LINK_TEXT, "FAQs").click()

        # Validate the current URL to check if the link works
        WebDriverWait(self.driver, 10).until(EC.url_contains("faqs"))
        current_url = self.driver.current_url
        assert current_url == "https://smoothmaths.co.uk/faqs/", f"Unexpected URL: {current_url}"

        # Test each FAQ toggle, ensuring all expand and collapse
        faq_items = [
            ".et_pb_accordion_item_1 > .et_pb_toggle_title",
            ".et_pb_accordion_item_2 > .et_pb_toggle_title",
            ".et_pb_accordion_item_3 > .et_pb_toggle_title",
            ".et_pb_accordion_item_4 > .et_pb_toggle_title",
            ".et_pb_accordion_item_5 > .et_pb_toggle_title",
            ".et_pb_accordion_item_6 > .et_pb_toggle_title"
        ]
        
        for faq in faq_items:
            self.driver.find_element(By.CSS_SELECTOR, faq).click()
            time.sleep(1)  # Optional: Wait to ensure the animation completes

        # Take a screenshot after all FAQs have been clicked
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = f"screenshots/faqs_test_{timestamp}.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        self.driver.save_screenshot(screenshot_path)
        
        # Assert the screenshot is saved successfully
        assert os.path.exists(screenshot_path), "Screenshot not saved!"

