from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class TransactionOps:
    def __init__(self, webdriver):
        self.webdriver = webdriver

    def auto_allocate(self):
        try:
            self.webdriver.click(By.NAME, "realloc_trid")
            self.webdriver.click(By.NAME, "update")
        except NoSuchElementException:
            pass

    def allocate_cents(self, amount):
        self.scrape_transaction()
        try:
            if self.charge_equals_top_value():
                self.subtract_current_allocation(
                    amount,
                )
                self.webdriver.send_keys_element(
                    self.additional_rent_element, amount, True
                )
            if self.top_allocation_value == 0:
                self.webdriver.send_keys_element(
                    self.top_allocation_element, amount, True
                )
        except:
            pass

    def charge_equals_top_value(self):
        if self.full_charge == self.top_allocation_value:
            return True

    def subtract_top_allocation(self, amount):
        new_allocation = round(self.top_allocation_value - amount, 2)
        self.webdriver.send_keys_element(
            self.top_allocation_element, new_allocation, True
        )

    def subtract_compliance_from_rent(self, compliance_amount):
        self.scrape_transaction()
        if self.charge_equals_top_value():
            self.subtract_current_allocation(compliance_amount)

    def allocation_elements(self, num):
        try:
            return self.webdriver.driver.find_element(
                By.XPATH,
                f"/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{num}]/td[2]/form/input[4]",
            )
        except NoSuchElementException:
            return False

    def scrape_transaction(self):
        try:
            self.full_charge = float(
                self.webdriver.driver.find_element(
                    By.XPATH,
                    "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input",
                ).get_attribute("value")
            )
        except NoSuchElementException:
            self.full_charge = float(
                self.webdriver.driver.find_element(
                    By.XPATH,
                    "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/form/table[1]/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/input",
                ).get_attribute("value")
            )
        self.top_allocation_element = self.allocation_elements(2)
        self.top_allocation_value = float(
            self.top_allocation_element.get_attribute("value")
        )
        self.additional_rent_element = self.allocation_elements(3)

    def allocate_amount(self, amount):
        self.webdriver.send_keys(
            By.XPATH,
            "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/form/input[4]",
            amount,
            True,
        )
