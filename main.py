import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CookieClickerBot:
    def __init__(self, driver_path):
        """
        Initialize the Cookie Clicker Bot
        :param driver_path: Path to the Microsoft Edge WebDriver executable
        """
        # Set up Edge options
        edge_options = Options()
        # Uncomment the line below if you want to run in headless mode
        # edge_options.add_argument("--headless")

        # Set up the Edge WebDriver service
        self.service = Service(driver_path)

        # Create the WebDriver instance
        self.driver = webdriver.Edge(service=self.service, options=edge_options)

        # Wait utility
        self.wait = WebDriverWait(self.driver, 10)

    def start_game(self):
        """
        Navigate to the Cookie Clicker game
        """
        self.driver.get("https://orteil.dashnet.org/experiments/cookie/")
        print("Game loaded successfully!")

    def click_cookie(self, num_clicks=100):
        """
        Click the big cookie repeatedly
        :param num_clicks: Number of times to click the cookie
        """
        cookie = self.wait.until(EC.element_to_be_clickable((By.ID, "cookie")))

        for _ in range(num_clicks):
            cookie.click()

    def buy_upgrades(self):
        """
        Buy available upgrades and products
        """
        # List of upgrade priorities (from most expensive to least)
        upgrade_ids = [
            "buyTime machine",
            "buyPortal",
            "buyAlchemy lab",
            "buyShipment",
            "buyMine",
            "buyFactory",
            "buyGrandma",
            "buyCursor",
        ]

        for upgrade_id in upgrade_ids:
            try:
                # Find the upgrade element
                upgrade = self.driver.find_element(By.ID, upgrade_id)

                # Check if the upgrade is enabled (not grayed out)
                if "grayed" not in upgrade.get_attribute("class"):
                    upgrade.click()
                    print(f"Bought {upgrade_id.replace('buy', '')}")
            except Exception as e:
                # Silently pass if upgrade not found or can't be bought
                pass

    def check_cookies_per_second(self):
        """
        Check and print current cookies per second
        """
        try:
            cps = self.driver.find_element(By.ID, "cps").text
            print(f"Cookies per second: {cps}")
        except Exception as e:
            print("Could not retrieve cookies per second")

    def run_bot(self, runtime_minutes=15):
        """
        Run the bot for a specified duration
        :param runtime_minutes: How long to run the bot
        """
        start_time = time.time()
        end_time = start_time + (runtime_minutes * 60)

        print(f"Starting Cookie Clicker Bot for {runtime_minutes} minutes")

        while time.time() < end_time:
            # Click the cookie
            self.click_cookie(10)

            # Buy upgrades periodically
            self.buy_upgrades()

            # Check cookies per second
            self.check_cookies_per_second()

            # Small pause to prevent overwhelming the browser
            time.sleep(0.1)

        print("Bot run complete!")

    def cleanup(self):
        """
        Close the browser
        """
        self.driver.quit()


def main():
    # Replace with the path to your Edge WebDriver executable
    EDGE_DRIVER_PATH = r"msedgedriver.exe"

    # Create bot instance
    bot = CookieClickerBot(EDGE_DRIVER_PATH)

    try:
        # Start the game
        bot.start_game()

        # Run the bot for 15 minutes
        bot.run_bot(runtime_minutes=15)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Always close the browser
        bot.cleanup()


if __name__ == "__main__":
    main()
