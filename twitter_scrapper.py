import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from typing import List, Optional, Dict
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Fixed the __name__ syntax


class TwitterScraper:
    def __init__(self, username: str, password: str, headless: bool = False):
        self.username = username
        self.password = password

        # Enhanced Chrome options to avoid detection
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-blink-features")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Add random user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]
        options.add_argument(f'user-agent={random.choice(user_agents)}')

        if headless:
            options.add_argument('--headless=new')
            options.add_argument('--window-size=1920,1080')

        try:
            # Initialize the driver with additional preferences
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)

            # Execute CDP commands to prevent detection
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": random.choice(user_agents)
            })

            # Execute JavaScript to prevent detection
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            self.wait = WebDriverWait(self.driver, 20)
            logger.info("Browser initialized successfully")

            # Add random delay to mimic human behavior
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            logger.error(f"Failed to initialize browser: {str(e)}")
            raise

    def add_random_delay(self):
        """Add random delay to mimic human behavior"""
        time.sleep(random.uniform(0.5, 2))

    def login(self):
        """Login to Twitter account with enhanced anti-detection measures"""
        try:
            # Navigate to Twitter login page with random delay
            logger.info("Navigating to Twitter login page")
            self.driver.get('https://twitter.com/i/flow/login')
            self.add_random_delay()

            # Find and input username with human-like typing
            logger.info("Attempting to enter username")
            username_input = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
            )
            self.type_like_human(username_input, self.username)
            self.add_random_delay()
            username_input.send_keys(Keys.ENTER)
            logger.info("Username entered successfully")

            # Find and input password with human-like typing
            logger.info("Attempting to enter password")
            password_input = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
            )
            self.type_like_human(password_input, self.password)
            self.add_random_delay()
            password_input.send_keys(Keys.ENTER)
            logger.info("Password entered successfully")

            # Random delay before verification
            time.sleep(random.uniform(3, 5))

            # Verify login success
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='primaryColumn']")))
                logger.info("Login successful!")
                return True
            except Exception as e:
                logger.error(f"Login verification failed: {str(e)}")
                self.save_screenshot("login_failed.png")
                return False

        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            self.save_screenshot("login_error.png")
            return False

    def type_like_human(self, element, text):
        """Type text with random delays between keystrokes to mimic human behavior"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

    def save_screenshot(self, filename: str):
        """Save screenshot for debugging"""
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved as {filename}")
        except Exception as e:
            logger.error(f"Failed to save screenshot: {str(e)}")

    def get_trending_topics(self, limit: int = 5) -> List[str]:
        """Fetch trending topics from Twitter homepage"""
        trending_topics = []
        try:
            logger.info("Waiting for trending section to load")
            # Wait for trending section
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='trend']"))
            )
            time.sleep(3)

            # Find all trending topics
            topics = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='trend']")
            logger.info(f"Found {len(topics)} trending topics")

            # Extract the text from each trending topic
            for topic in topics[:limit]:
                try:
                    topic_text = topic.text.split('\n')[0]
                    trending_topics.append(topic_text)
                except Exception as e:
                    logger.error(f"Error extracting topic text: {str(e)}")
                    continue

            logger.info(f"Successfully extracted {len(trending_topics)} topics")

        except Exception as e:
            logger.error(f"Error fetching trending topics: {str(e)}")
            self.save_screenshot("trending_error.png")

        return trending_topics

    def close(self):
        """Close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")