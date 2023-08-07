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
