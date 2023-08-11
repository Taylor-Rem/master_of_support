from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


class ResmapOperations:
    def __init__(self, webdriver, scrape):
        self.webdriver = webdriver
        self.scrape = scrape

    def open_property(self, property):
        self.webdriver.click(By.XPATH, "//a[contains(., 'CHANGE PROPERTY')]")
        self.webdriver.click(By.XPATH, f"//a[contains(., '{property}')]")

    def open_unit(self, unit):
        self.webdriver.send_keys(By.NAME, "search_input", unit + Keys.ENTER)

    def open_ledger(self):
        self.webdriver.click(By.XPATH, ".//a[text()='Ledger']")

    def search_resident(self, resident, num):
        self.webdriver.click(
            By.ID,
            f"former{num}",
        )
        self.webdriver.send_keys(By.NAME, "ressearch", resident + Keys.ENTER)

    def compare_resident(self, resident):
        RM_resident = self.scrape.scrape_resident()
        if RM_resident and resident:
            if resident in RM_resident:
                return True
            else:
                return False
        return False

    def open_unit_and_ledger(self, unit, resident):
        self.open_unit(unit)
        if self.compare_resident(resident) or resident is None:
            self.open_ledger()
        else:
            self.open_former_ledger(unit, resident)

    def search_resident_and_open_ledger(self, resident):
        try:
            self.search_resident(resident, 1)
            self.open_ledger()
        except NoSuchElementException:
            self.search_resident(resident, 2)
            self.open_ledger()

    def open_former_ledger(self, unit, resident):
        try:
            self.webdriver.click(By.XPATH, f".//a[text()='{unit}']")
            self.webdriver.click(
                By.XPATH,
                "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[2]/td[5]/a",
            )
            self.click_last_ledger()
        except NoSuchElementException:
            self.search_resident_and_open_ledger(resident)

    def click_last_ledger(self):
        table = self.webdriver.driver.find_element(
            By.XPATH,
            "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody",
        )
        ledger_links = table.find_elements(By.XPATH, ".//a[text()='Ledger']")
        if ledger_links:
            self.webdriver.click_element(ledger_links[-1])
        else:
            self.open_ledger()


class ManageportalOps:
    def __init__(self, webdriver):
        self.webdriver = webdriver

    def resolve_ticket(self, icon, back):
        self.webdriver.click(By.XPATH, "//button[contains(., 'Change Ticket Status')]")

        self.click_button("button", icon)

        if back:
            self.click_button("a", back)

    def click_button(self, element_type, icon):
        xpath = f"//{element_type}[.//i[contains(@class, 'material-icons') and text()='{icon}']]"
        self.webdriver.wait_click(By.XPATH, xpath)
        self.webdriver.click(By.XPATH, xpath)
