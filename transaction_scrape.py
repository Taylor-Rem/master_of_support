from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class TransactionScrape:
    def __init__(self, webdriver):
        self.webdriver = webdriver

    def scrape_transaction(self):
        full_charge = float(
            self.webdriver.driver.find_element(
                By.XPATH,
                "//input[@type='text' and @name='amount']",
            ).get_attribute("value")
        )
        top_allocation_element = self.allocation_elements(2)
        top_allocation_value = float(top_allocation_element.get_attribute("value"))
        additional_rent_element = self.allocation_elements(3)
        return (
            full_charge,
            top_allocation_element,
            top_allocation_value,
            additional_rent_element,
        )

    def allocation_elements(self, num):
        try:
            return self.webdriver.driver.find_element(
                By.XPATH,
                f"/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{num}]/td[2]/form/input[4]",
            )
        except NoSuchElementException:
            return False
