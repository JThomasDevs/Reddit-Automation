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
        # THIS FUNCTION DOES NOT WORK RIGHT NOW - IT WON'T CLICK THE SUBMIT BUTTON
        # TODO: Look into using the modern reddit registration page as opposed to old.reddit.com

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
        self.driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border').click()
        for i in range(60):
            print(i+1)
            time.sleep(1)
        self.driver.switch_to.default_content()
        self.driver.find_element(By.CLASS_NAME, 'c-btn c-btn-primary c-pull-right').click()
        with open('reddit-accounts.txt', 'a') as accounts:
            accounts.write(f'{self.username}:{self.password}:{self.username}')

        print("Account created!")
        time.sleep(1000)

    def login(self):
        print('Logging in...')
        self.driver.get('https://old.reddit.com/')
        self.driver.find_element(By.NAME, 'user').send_keys(self.username)
        self.driver.find_element(By.NAME, 'passwd').send_keys(self.password)
        self.driver.find_element(By.CLASS_NAME, 'submit').click()
        print("Logged in!")
        time.sleep(1)

    def target(self, subreddit):
        print(f'Targeting r/{subreddit}')
        target = f'https://old.reddit.com/r/{subreddit}'
        self.driver.get(target)
        time.sleep(1)

    def upvote(self):
        print('Upvoting...')
        self.driver.find_element(By.CLASS_NAME, 'arrow up login-required access-required').click()
        print('Upvoted!')
        time.sleep(1000)

    def downvote(self):
        print('Downvoting...')
        self.driver.find_element(By.CLASS_NAME, 'arrow down login-required access-required').click()
        print('Downvoted!')
        time.sleep(1000)