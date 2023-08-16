from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from selenium.webdriver.common.action_chains import ActionChains
import re

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
        self.wait = WebDriverWait(self.driver, 10)
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

    def wait_page_load(self):
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def wait_click(self, by, value):
        self.wait.until(EC.element_to_be_clickable((by, value)))

    def get_number_from_string(self, text):
        match = re.search(r"\$\s*([\d\.]+)", text)
        if match:
            return float(match.group(1))
        else:
            return None

    def return_elements(self, name):
        try:
            elements = self.driver.find_elements(By.XPATH, f'//a[text()="{name}"]')
        except:
            return None

    def return_last_element(self, name):
        try:
            elements = self.driver.find_elements(
                By.XPATH, f"//a[contains(., '{name}')]"
            )
            if elements:
                return elements[-1]
            else:
                return self.driver.find_element(By.XPATH, f"//a[contains(., '{name}')]")
        except NoSuchElementException:
            pass

    def element_status(self, by, value):
        try:
            element = self.driver.find_element(
                by,
                value,
            )
            return True
        except NoSuchElementException:
            return False

    def return_element(self, by, value):
        try:
            element = self.driver.find_element(by, value)
            return element.get_attribute("innerHTML").strip()
        except NoSuchElementException:
            return None

    def send_keys(self, by, value, keys, enter=False):
        try:
            element = self.driver.find_element(by, value)
            self.send_keys_element(element, keys, enter)
        except NoSuchElementException:
            pass

    def send_keys_element(self, element, keys, enter=False):
        try:
            element.clear()
            element.send_keys(keys)
            if enter:
                element.send_keys(Keys.ENTER)
        except NoSuchElementException:
            pass

    def click(self, by, value):
        element = self.driver.find_element(by, value)
        if element:
            self.click_element(element)
        else:
            raise NoSuchElementException(f"Element not found with {by} = {value}")

    def click_element(self, element):
        try:
            if element is not None and self.is_clickable(element):
                self.scroll_to_element(element)
                element.click()
            else:
                pass
        except NoSuchElementException:
            pass

    def is_clickable(self, element):
        is_clickable = element.is_displayed() and element.is_enabled()
        return element and is_clickable == True

    def scroll_to_element(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

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
            self.send_keys(By.NAME, "password", password, True)
        except NoSuchElementException:
            pass

    def open_program(self, site):
        self.driver.get(site)
        self.login(username, password)

    def go_back(self, current_url):
        if not self.check_webpage(current_url):
            self.driver.back()

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
