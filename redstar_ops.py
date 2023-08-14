from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from transaction_ops import TransactionOps


class RedstarOps:
    def __init__(self, webdriver, resmap_ops):
        self.webdriver = webdriver
        self.resmap_ops = resmap_ops
        self.transaction_ops = TransactionOps(webdriver)

    def retrieve_amount_from_bottom(self, row):
        try:
            cells = row.find_all("td")
            amount = cells[1].get_text(strip=True)
            return self.webdriver.get_number_from_string(amount)
        except:
            return None

    def scrape_page(self):
        prepaid_rent_amount = self.webdriver.get_number_from_string(
            self.webdriver.return_element(
                By.XPATH,
                "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[3]/td[5]",
            )
        )
        current_url = self.webdriver.driver.current_url
        current_month_rows = self.resmap_ops.get_rows(
            self.resmap_ops.tables["current_month"]
        )
        bottom_rows = self.resmap_ops.get_rows(self.resmap_ops.tables["bottom"])
        return prepaid_rent_amount, current_url, current_month_rows, bottom_rows

    def reallocate_rule_compliance(self, compliance_amount, current_url):
        self.webdriver.click_element(self.webdriver.return_last_element("Rent"))
        self.transaction_ops.subtract_compliance_from_rent(compliance_amount)
        self.webdriver.go_back(current_url)

    def allocate_all_credits(self, amount, element):
        if amount.startswith("(") or amount.endswith(")"):
            self.webdriver.click_element(element)
            self.transaction_ops.auto_allocate()

    def allocate_cents(self, amount_num, prepaid_amount):
        if amount_num == prepaid_amount:
            try:
                self.webdriver.click_element(
                    self.webdriver.return_last_element("Home Rental")
                )
                self.transaction_ops.allocate_cents(amount_num)
            except:
                self.webdriver.click_element(self.webdriver.return_last_element("Rent"))
                self.transaction_ops.allocate_cents(amount_num)

    def bottom_ops(self, transaction, amount, bottom_row):
        bottom_amount = self.retrieve_amount_from_bottom(bottom_row)
        if bottom_amount == amount:
            self.webdriver.click_element(
                self.webdriver.return_last_element(transaction)
            )
            self.transaction_ops.allocate_amount(amount)
