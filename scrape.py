from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class Scrape:
    # XPATHs

    def __init__(self, webdriver):
        self.ticket_property_xpath = "/html/body/div[1]/div[19]/div/main/div/div/div/div/div[2]/div/div/table/tbody/tr[6]/td[2]/strong/a"
        self.ticket_unit_xpath = "/html/body/div[1]/div[19]/div/main/div/div/div/div/div[2]/div/div/table/tbody/tr[11]/td[2]/a/strong"
        self.ticket_resident_xpath = "/html/body/div[1]/div[19]/div/main/div/div/div/div/div[2]/div/div/table/tbody/tr[12]/td[2]/a/strong"

        self.webdriver = webdriver

    def scrape_ticket(self):
        try:
            property = self.webdriver.return_element(
                By.XPATH, self.ticket_property_xpath
            )
        except NoSuchElementException:
            property = None

        try:
            unit = self.webdriver.return_element(By.XPATH, self.ticket_unit_xpath)
        except NoSuchElementException:
            unit = None
        try:
            resident = self.webdriver.return_element(
                By.XPATH, self.ticket_resident_xpath
            )
        except NoSuchElementException:
            resident = None

        return property, unit, resident

    def scrape_resident(self):
        try:
            RM_resident = self.webdriver.return_element(
                By.XPATH,
                "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/a",
            )
            return RM_resident
        except:
            return None
