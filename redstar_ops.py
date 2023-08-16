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

    def reallocate_rule_compliance(self, compliance_amount, current_url):
        self.webdriver.click_element(self.webdriver.return_last_element("Rent"))
        self.transaction_ops.subtract_compliance_from_rent(compliance_amount)
        self.webdriver.go_back(current_url)

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
