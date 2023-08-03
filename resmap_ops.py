from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


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
        self.webdriver.click(
            By.XPATH,
            "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[last()]/td[4]/a[4]",
        )

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
            self.search_resident_and_open_ledger(resident)

    def search_resident_and_open_ledger(self, resident):
        try:
            self.search_resident(resident, 2)
            self.open_ledger()
        except NoSuchElementException:
            self.search_resident(resident, 1)
            self.open_ledger()
