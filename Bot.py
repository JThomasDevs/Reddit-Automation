import time

from selenium.common import ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from Crawler import Crawler


class RedditBot(Crawler):

    def __init__(self):
        super().__init__()
        self.username = None
        self.email = None
        self.password = None

    def create_account(self):
        """Creates a Reddit account using a randomly generated username, email, and password."""
        # TODO: This function /should/ work properly, but more testing is still needed.

        print('Creating account...')
        self.driver.get('https://www.reddit.com/register')

        # Set account info
        self.username = self.rand_username()
        while len(self.username) > 20:
            self.username = self.rand_username()
        self.email = self.username + '@gmail.com'
        self.password = self.rand_pass()

        # Begin info input
        self.driver.find_element(By.NAME, 'email').send_keys(self.email)
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(self.username)
        self.driver.find_element(By.NAME, 'password').send_keys(self.password)
        time.sleep(1)
        self.driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div[3]/button').click()
        print('Clicked submit button')
        time.sleep(5)

        # While the recaptcha checkbox is not checked
        while 'register' in self.driver.current_url:
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '//iframe[starts-with(@name,"a-") and starts-with(@src,"https://www.google.com/recaptcha")]'))
            self.driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border').click()
            print('Clicked recaptcha checkbox')

            # Wait to manually complete captcha
            for i in range(60):
                print(i+1)
                time.sleep(1)
                # Translation: If the recaptcha checkbox is checked, break
                if self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[1]/div/div/span').get_attribute('aria-checked') == 'true':
                    break
            if self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[1]/div/div/span').get_attribute(
                    'aria-checked') == 'true':
                break

        # Submit again
        self.driver.switch_to.default_content()
        self.driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div[3]/button').click()
        print('Clicked submit button again')

        # Wait for account creation to be confirmed
        while 'signup_survey' not in self.driver.current_url:
            # Sometimes, too many accounts have been created in too short of a time
            if self.driver.find_element(By.CLASS_NAME, 'AnimatedForm__submitStatus m-error').is_displayed():
                print('Too many accounts created recently. Wait about 10 minutes and try again.')
            if 'signup_survey' in self.driver.current_url:
                break
            time.sleep(1)

        # Write account info to file
        with open('reddit-accounts.txt', 'a') as accounts:
            accounts.write(f'\n{self.username}:{self.password}:{self.username}')

        print("Account created!")
        time.sleep(1000)

    def login(self):
        """Log in to Reddit so that your bot may perform actions on the website"""

        print('Logging in...')
        self.driver.get('https://old.reddit.com/')
        self.driver.find_element(By.NAME, 'user').send_keys(self.username)
        self.driver.find_element(By.NAME, 'passwd').send_keys(self.password)
        self.driver.find_element(By.CLASS_NAME, 'submit').click()
        print("Logged in!")
        time.sleep(1)

    def target(self, subreddit):
        """This function navigates to the specified subreddit"""

        print(f'Targeting r/{subreddit}')
        target = f'https://www.reddit.com/r/{subreddit}'
        self.driver.get(target)
        time.sleep(1)

    def downvote_bomb(self, num_posts: int):
        """Downvotes the first {num_posts} posts on the page that are not already downvoted.
        This function may break if you try to downvote too many posts at once"""

        pressed = 0
        post_ids = []

        while pressed < num_posts:
            # Find all posts on the page
            posts = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid = post-container]')
            for post in posts:
                # Skip out of range posts that are still loaded in the HTML
                if post.get_attribute('id') in post_ids:
                    continue
                # If the post is already downvoted, skip it
                if post.find_element(By.CSS_SELECTOR, 'button[aria-label="downvote"]').get_attribute(
                        'aria-pressed') == 'true':
                    continue
                # Downvote the post
                try:
                    post.find_element(By.CSS_SELECTOR, 'button[aria-label="downvote"]').click()
                    pressed += 1
                    post_ids.append(post.get_attribute('id'))
                    print(pressed)
                except ElementClickInterceptedException:
                    continue
                except ElementNotInteractableException:
                    continue
                if pressed == num_posts:
                    break
            time.sleep(5)

        if pressed == 0:
            print('No posts to downvote')
        else:
            print(f'Downvoted {pressed} posts')

    def upvote_bomb(self, num_posts: int):
        """Upvotes the first {num_posts} posts on the page that are not already upvoted.
        This function may break if you try to upvote too many posts at once"""

        pressed = 0
        post_ids = []

        while pressed < num_posts:
            # Find all posts on the page
            posts = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid = post-container]')
            for post in posts:
                # Skip out of range posts that are still loaded in the HTML
                if post.get_attribute('id') in post_ids:
                    continue
                # If the post is already upvoted, skip it
                if post.find_element(By.CSS_SELECTOR, 'button[aria-label="upvote"]').get_attribute(
                        'aria-pressed') == 'true':
                    continue
                # Upvote the post
                try:
                    post.find_element(By.CSS_SELECTOR, 'button[aria-label="upvote"]').click()
                    pressed += 1
                    post_ids.append(post.get_attribute('id'))
                    print(pressed)
                except ElementClickInterceptedException:
                    continue
                except ElementNotInteractableException:
                    continue
                if pressed == num_posts:
                    break
            time.sleep(5)

        if pressed == 0:
            print('No posts to upvote')
        else:
            print(f'upvoted {pressed} posts')

    def quit(self):
        """Shut everything down once you're done"""
        self.driver.quit()
