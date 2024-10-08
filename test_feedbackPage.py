import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

# CSV file path to store test results (optional)
CSV_FILE_PATH = "test_results.csv"

class TestFeedbackPage():
    def setup_method(self, method):
        # Use headless Chrome for CI
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_feedbackPage(self):
        start_time = time.time()
        
        # Navigate to the feedback page
        self.driver.get("https://smoothmaths.co.uk/")
        self.driver.set_window_size(1296, 696)
        self.driver.execute_script("window.scrollTo(0,94)")
        self.driver.find_element(By.LINK_TEXT, "Feedback").click()
        self.driver.execute_script("window.scrollTo(0,148)")

        # Fill in the feedback form
        self.driver.find_element(By.ID, "wpforms-21990-field_2").send_keys("Hanzila")
        self.driver.find_element(By.ID, "wpforms-21990-field_5").send_keys("testig")
        self.driver.find_element(By.ID, "wpforms-21990-field_4_5").click()
        self.driver.find_element(By.ID, "wpforms-submit-21990").click()

        # Wait for the confirmation message to appear
        try:
            # Update the selector to the correct confirmation message element
            confirmation_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".wpforms-confirmation-container-full p"))
            )
            assert "Thanks for leaving a review" in confirmation_message.text

            # Save screenshot with timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/feedback_confirmation_{timestamp}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            self.driver.save_screenshot(screenshot_path)

            # Optional: Store the test results in a CSV file
            self._store_test_results("Test Feedback Page", "Passed", screenshot_path)

        except Exception as e:
            # If the text is not found, raise an error and fail the test
            end_time = time.time()
            duration = end_time - start_time
            print(f"Test failed: {e}. Test duration: {duration:.2f} seconds")
            raise AssertionError("The confirmation message did not appear as expected.")

    def _store_test_results(self, test_case, status, screenshot_path):
        # Optional: Save test results in a CSV file
        import pandas as pd
        results = {
            "Test Case": [test_case],
            "Status": [status],
            "Screenshot": [screenshot_path]
        }
        df = pd.DataFrame(results)
        if not os.path.exists(CSV_FILE_PATH):
            df.to_csv(CSV_FILE_PATH, index=False)
        else:
            df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)

