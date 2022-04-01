from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_condictions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from custom_logger import set_logger

logger = set_logger("selenium_stats")

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome Options for headless browser is enabled.
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

def register_voter( url: str,
                    chrome_options: Options
                    ) -> None:

    """Registers a voter for the contest with bogus names and email.
       Email Agent is used with GuerrilaMail API.
       0. Generate user + email
       1. Navigates to the specific URL
       2. Connects to the redirected link
       3. "Finds element by ID with text 'vote for Kade'
       4. Clicks element ID
       5. Inputs generated firstlast@guerrilamail-alt.com, First, Last
       6. Submit form
       7. Retrieve mfa code
       8. Resubmit form with mfa code
    """
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(800,600)
        driver.get(url)
        WebDriverWait(driver, 10).until(
                EC.title_contains("Voting")
                )
        driver.find_element_by_class_name('voteBtn votable').click()
        driver.find_element_by_css_selector(".ng-pristine ng-untouched ng-valid[placeholder='Email Address']").send_keys(email)
        driver.find_element_by_css_selector(".ng-pristine ng-untouched ng-valid[placeholder='First Name']").send_keys(fname)
        driver.find_element_by_css_selector(".ng-pristine ng-untouched ng-valid[placeholder='Last Name']").send_keys(lname)
        driver.find_element_by_class_name('emailLoginBtn ng-binding').click()

        return driver
    except Exception as shit:
        logger.error(f"{shit} happened.")
        return None
    finally:
        driver.quit()


if __name__ == "__main__":
    url = "https://ul.ink/13ZSA-V6GA"
    options = set_chrome_options
    session = register_voter(url, options)
    print(session)
