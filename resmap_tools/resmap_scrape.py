from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


class ResmapScrape:
    # XPATHs

    def __init__(self, webdriver):
        self.webdriver = webdriver

    def scrape_ticket(self):
        try:
            property = self.webdriver.return_element(
                By.XPATH,
                "//tr/td[@class='text-xs-right' and contains(text(), 'Property')]/following-sibling::td[@class='text-xs-left']/strong/a",
            )
        except NoSuchElementException:
            property = None

        try:
            unit = self.webdriver.return_element(
                By.XPATH,
                "//tr/td[@class='text-xs-right' and contains(text(), 'Space')]/following-sibling::td[@class='text-xs-left']/a/strong",
            )
        except NoSuchElementException:
            unit = None
        try:
            resident = self.webdriver.return_element(
                By.XPATH,
                "//tr/td[@class='text-xs-right' and contains(text(), 'Resident')]/following-sibling::td[@class='text-xs-left']/a/strong",
            )
        except NoSuchElementException:
            resident = None

        return property, unit, resident

    def scrape_resident(self):
        try:
            RM_resident = self.webdriver.return_element(
                By.XPATH,
                '//tbody/tr[2]/td[2]/a[contains(@href, "resident.php?cmd=viewresident")]',
            )
            return RM_resident
        except:
            return None

    def retrieve_transaction_and_amount(self, row):
        cells = row.find_all("td")
        transaction = cells[2].get_text(strip=True)
        amount = cells[3].get_text(strip=True)
        return transaction, amount

    def scrape_page(self):
        prepaid_rent_amount = self.webdriver.get_number_from_string(
            self.webdriver.return_element(
                By.XPATH,
                "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[3]/td[5]",
            )
        )
        current_url = self.webdriver.driver.current_url
        return prepaid_rent_amount, current_url

    def choose_table(self, num):
        return f"/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[last(){num}]/tbody/tr[2]/td/table/tbody"

    def define_table(self, by, value):
        table_elements = self.webdriver.driver.find_elements(by, value)
        table = [element.get_attribute("outerHTML") for element in table_elements]
        return table

    def get_rows(self, table):
        all_rows = []  # Initialize an empty list to collect all rows
        for table_html in table:
            soup = BeautifulSoup(table_html, "html.parser")
            rows = soup.find_all(
                "tr", class_=lambda value: value and value.startswith("td")
            )
            all_rows.extend(rows)  # Add rows to the list
        return all_rows  # Return the list of all rows
