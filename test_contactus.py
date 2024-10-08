import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

class TestContactus():
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
    
    def test_contactus(self):
        # Navigate to the Contact Us page
        self.driver.get("https://smoothmaths.co.uk/")
        self.driver.set_window_size(1296, 696)
        
        # Scroll down and click the "Contact us" link
        self.driver.execute_script("window.scrollTo(0, 390)")
        self.driver.execute_script("window.scrollTo(0, 2384)")
        self.driver.find_element(By.LINK_TEXT, "Contact us").click()
        self.driver.execute_script("window.scrollTo(0, 155.3333282470703)")
        
        # Fill the contact form
        self.driver.find_element(By.ID, "et_pb_contact_name_0").send_keys("Hanzila")
        self.driver.find_element(By.ID, "et_pb_contact_email_0").send_keys("hanzila@dovidigital.com")
        self.driver.find_element(By.ID, "et_pb_contact_message_0").send_keys("Testing")
        
        # Extract the captcha equation, solve it, and fill it in
        captcha_question = self.driver.find_element(By.CSS_SELECTOR, ".et_pb_contact_captcha_question").text
        captcha_answer = self.solve_captcha(captcha_question)
        self.driver.find_element(By.NAME, "et_pb_contact_captcha_0").send_keys(captcha_answer)
        
        # Submit the form
        self.driver.find_element(By.NAME, "et_builder_submit_button").click()

        # Wait for the success message to appear
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".et_pb_contact_form_0 .et_pb_contact_message p"))
        )
        
        # Capture screenshot
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = f"screenshots/contact_us_{timestamp}.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        self.driver.save_screenshot(screenshot_path)

        # Verify the success message
        success_message = self.driver.find_element(By.CSS_SELECTOR, ".et_pb_contact_form_0 .et_pb_contact_message p").text
        assert success_message == "Thanks for contacting us", "Expected message not found!"

    def solve_captcha(self, captcha_question):
        # Example: if captcha_question is "7 + 12", this will split it, calculate the answer, and return it.
        numbers = captcha_question.split(" + ")
        result = int(numbers[0]) + int(numbers[1])
        return str(result)
