from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

from guerrillamail import GuerrillaMailSession

from custom_logger import set_logger
import random

logger = set_logger("selenium_stats")

class Voter:
    def __init__(self, fname, lname, email, session):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.session = session
def create_email(email):
    session = GuerrillaMailSession()
    session.set_email_address(email)
#    print (session.get_session_state()['email_address'])
#    print (session.get_email_list()[0].guid)

    return session

def generate_voters(num: int) -> list:

    voters = []
    fnames = []
    lnames = []
    
    with open('./fname.txt', 'r') as f:
        for line in f:
            fnames.append(line.strip())
    with open('./lname.txt', 'r') as f:
        for line in f:
            lnames.append(line.strip())
    
    for i in range(0,num):
        
        fn  = random.choice(fnames)
        ln  = random.choice(lnames)
        s   = create_email(("{}{}".format(fn, ln)).lower())
        em  = (s.get_session_state()['email_address'])

        voters.append(Voter(fn,ln,em,s))

    return voters

def set_chrome_options():
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
                    chrome_options: Options,
                    voter
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
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(800,600)
    
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/div[4]/div[1]"))
                )
        driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/div[4]/div[1]").click()
        driver.find_element(By.XPATH, "/html/body/div[9]/div[2]/div/div[2]/form/input[1]").send_keys(voter.email)
        driver.find_element(By.XPATH, "/html/body/div[9]/div[2]/div/div[2]/form/input[2]").send_keys(voter.fname)
        driver.find_element(By.XPATH, "/html/body/div[9]/div[2]/div/div[2]/form/input[3]").send_keys(voter.lname)
        driver.find_element(By.XPATH, "/html/body/div[9]/div[2]/div/div[2]/form/button").submit()

        return driver

    except Exception as shit:

        logger.error(f"{shit} happened.")
        return None

    finally:
        print('{} voted'.format(voter.email))
        driver.close()


if __name__ == "__main__":
    
    url = "https://campaign.aptivada.com/gallery/1179434?id=1179434&type=gallery&entry_id=V6GA&embed=true&parent=https%253A%252F%252Fhitscarolina.iheart.com%252Fpromotions%252Fvoting-carolina-s-cutest-baby-bracket-contest-1179434%252F%253Fapt_id%253D1179434%2526apt_type%253Dgallery%2526apt_entry_id%253DV6GA"
    votes = 1

    options = set_chrome_options()
    voters = generate_voters(votes)
    
    for voter in voters:
       # print(voter.email)
       session = register_voter(url, options, voter)
       print('All done.')
    
