import time

from selenium.webdriver.common.by import By

from Crawler import Crawler


class RedditBot(Crawler):

    def __init__(self):
        super().__init__()
        self.username = None
        self.email = None
        self.password = None

    def create_account(self):
        print('Creating account...')
        self.driver.get('https://old.reddit.com/register')

        # Set account info
        self.username = self.rand_username()
        self.email = self.username + '@gmail.com'
        self.password = self.rand_pass()
        # Send the info to the account creation form and submit the form
        self.driver.find_element(By.NAME, 'user').send_keys(self.username)
        self.driver.find_element(By.NAME, 'passwd').send_keys(self.password)
        self.driver.find_element(By.NAME, 'passwd2').send_keys(self.password)
        self.driver.find_element(By.NAME, 'email').send_keys(self.email)

        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '//iframe[starts-with(@name,"a-") and starts-with(@src,"https://www.google.com/recaptcha")]'))
        captcha_done = self.driver.find_element(By.ID, 'recaptcha-anchor').get_attribute('aria-checked') == 'true'
        while not captcha_done:
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '//iframe[starts-with(@name,"a-") and starts-with(@src,"https://www.google.com/recaptcha")]'))
            self.driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border').click()
            time.sleep(5)
            self.driver.switch_to.default_content()
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        print("Account created!")
        time.sleep(1000)

    def login(self):
        print('Logging in...')
        self.driver.get('https://old.reddit.com/')
        self.driver.find_element(By.NAME, 'user').send_keys(self.username)
        self.driver.find_element(By.NAME, 'passwd').send_keys(self.password)
        self.driver.find_element(By.CLASS_NAME, 'submit').click()
        print("Logged in!")
        time.sleep(1000)