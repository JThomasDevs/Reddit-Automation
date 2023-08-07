import random
import string

from selenium.webdriver.chrome.options import Options
from undetected_chromedriver import Chrome

class Crawler:

    def __init__(self):
        # Initialize the names lists for the randomizer
        self.first_names = []
        self.last_names = []
        with open('firstnames.txt', 'r') as firstnames:
            for line in firstnames:
                name = line.strip()
                self.first_names.append(name)
        with open('lastnames.txt', 'r') as lastnames:
            for line in lastnames:
                name = line.strip()
                self.last_names.append(name)

        # Set browser settings and launch window when bot is created
        self.options = Options()
        self.options.add_argument('--ignore-certificate-errors')
        #self.options.add_argument('--headless=new')
        self.options.add_argument('--fullscreen')
        self.options.add_argument('--disk-cache-size=0')
        self.options.set_capability('acceptSSLCerts', True)
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--incognito')
        self.driver = Chrome(options=self.options)
        self.driver.implicitly_wait(10)

    def rand_username(self):
        first_index = random.randint(0, len(self.first_names) - 1)
        first_name = self.first_names[first_index]
        last_index = random.randint(0, len(self.last_names) - 1)
        last_name = self.last_names[last_index]
        nums = str(random.randint(0, 9999))
        if nums == 0:
            nums = ''
        username = f'{first_name}{last_name}{nums}'
        return username

    def rand_pass(self):
        characters = string.ascii_letters + string.digits + string.hexdigits
        password = ''.join(random.choices(characters, k=12))
        return password