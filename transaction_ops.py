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
            current_allocation_element = self.allocation_elements(2)
            current_allocation_value = float(
                current_allocation_element.get_attribute("value")
            )
            if self.full_charge == current_allocation_value:
                self.subtract_current_allocation(
                    current_allocation_element, current_allocation_value, amount
                )
                additional_rent_element = self.allocation_elements(3)
                self.webdriver.send_keys_element(additional_rent_element, amount, True)
            if current_allocation_value == 0:
                self.webdriver.send_keys_element(
                    current_allocation_element, amount, True
                )
        except:
            pass

    def subtract_current_allocation(
        self, current_allocation_element, current_allocation_value, amount
    ):
        new_allocation = round(current_allocation_value - amount, 2)
        self.webdriver.send_keys_element(
            current_allocation_element, new_allocation, True
        )

    def allocation_elements(self, num):
        return self.webdriver.driver.find_element(
            By.XPATH,
            f"/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{num}]/td[2]/form/input[4]",
        )

    def scrape_transaction(self):
        self.full_charge = float(
            self.webdriver.driver.find_element(
                By.XPATH,
                "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input",
            ).get_attribute("value")
        )

    def allocate_amount(self, amount):
        self.webdriver.send_keys(
            By.XPATH,
            "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/form/input[4]",
            amount,
            True,
        )
