from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from selenium.webdriver.common.action_chains import ActionChains

from config import username, password


class WebdriverOperations:
    _instance = None
    driver = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.driver = self.setup_webdriver()
        self.__initialized = True
        self.primary_tab = None
        self.res_map_url = "https://kingsley.residentmap.com/index.php"
        self.manage_portal_url = "https://residentmap.kmcmh.com/#/support_desk"

    def setup_webdriver(self):
        service = Service()
        options = webdriver.ChromeOptions()
        return webdriver.Chrome(service=service, options=options)

    def check_webpage(self, url):
        if self.driver.current_url != url:
            return False
        return True

    def return_element(self, by, value):
        try:
            element = self.driver.find_element(by, value)
            return element.get_attribute("innerHTML").strip()
        except NoSuchElementException:
            return None

    def send_keys(self, by, value, keys, enter=False):
        try:
            input = self.driver.find_element(by, value)
            input.clear()
            input.send_keys(keys)
            if enter:
                input.send_keys(Keys.ENTER)
        except NoSuchElementException:
            pass

    def click(self, by, value):
        try:
            element = self.driver.find_element(by, value)
            is_clickable = element.is_displayed() and element.is_enabled()
            actions = ActionChains(self.driver)
            if element and is_clickable:
                actions.move_to_element(element).perform()
                element.click()
        except NoSuchElementException:
            pass

    def new_tab(self):
        self.driver.execute_script("window.open('about:blank', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_primary_tab(self):
        if self.primary_tab is None:
            self.primary_tab = self.driver.window_handles[0]
        else:
            try:
                current_tab = self.driver.current_window_handle
                if current_tab != self.primary_tab:
                    self.driver.close()
            except NoSuchWindowException:
                pass
        self.driver.switch_to.window(self.primary_tab)

    def login(self, username, password):
        try:
            self.send_keys(By.NAME, "username", username)
            self.send_keys(By.NAME, "password", password, enter=True)
        except NoSuchElementException:
            pass

    def open_program(self, site):
        self.driver.get(site)
        self.login(username, password)

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
