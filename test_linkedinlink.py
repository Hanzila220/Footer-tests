import pytest
import time
import os
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLinkedinlink():
    def setup_method(self, method):
        # Set up headless Chrome for CI environments
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def wait_for_window(self, timeout=2):
        time.sleep(timeout)
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def test_linkedinlink(self):
        # Step 1: Navigate to the homepage
        self.driver.get("https://smoothmaths.co.uk/")
        self.driver.set_window_size(1296, 696)

        # Step 2: Scroll to the LinkedIn link in the footer
        self.driver.execute_script("window.scrollTo(0,1096.6666259765625)")
        self.vars["window_handles"] = self.driver.window_handles

        # Step 3: Click on the LinkedIn icon
        self.driver.find_element(By.CSS_SELECTOR, ".et_pb_social_media_follow_network_3_tb_footer > .icon").click()
        self.vars["win5507"] = self.wait_for_window(2)

        # Step 4: Switch to the new window
        self.driver.switch_to.window(self.vars["win5507"])

        # Step 5: Wait for the LinkedIn page to load and verify the URL
        WebDriverWait(self.driver, 10).until(EC.url_contains("linkedin.com"))
        current_url = self.driver.current_url
        assert current_url == "https://www.linkedin.com/company/smoothmathsuk/", f"Unexpected URL: {current_url}"

        # Step 6: Take a screenshot after loading the LinkedIn page
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = f"screenshots/linkedinlink_test_{timestamp}.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        self.driver.save_screenshot(screenshot_path)

        # Step 7: Assert the screenshot is saved
        assert os.path.exists(screenshot_path), "Screenshot not saved!"
