import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverManager:
    """Class to manage the setup of the Selenium WebDriver."""

    def __init__(self):
        self.driver = None

    def setup_driver(self, headless=False):
        """Sets up and returns a Chrome WebDriver instance."""
        chrome_options = Options()

        if headless:
            # Run in headless mode for better performance
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("log-level=3")

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(
                service=service, options=chrome_options)
            logging.info("Chrome WebDriver initialized successfully.")
            return self.driver
        except Exception as e:
            logging.error(f"Failed to initialize Chrome WebDriver: {e}")
            raise  # Re-raise exception after logging

    def quit_driver(self):
        """Quits the WebDriver instance."""
        if self.driver:
            logging.info("Quitting Chrome WebDriver.")
            self.driver.quit()
            self.driver = None
