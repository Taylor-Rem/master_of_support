from selenium.webdriver.common.by import By

from ledger_tools.credit_ops import CreditOps


class LedgerInteract:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.ledger_functions = LedgerFunctions(webdriver)

    def retrieve_rows(self, table_num=-5):
        table = self.resmap_ops.scrape.define_table(
            By.XPATH, self.resmap_ops.scrape.choose_table(table_num)
        )
        return self.resmap_ops.scrape.get_rows(table)

    def loop_through_table(self, operation, is_concession=False):
        rows = self.retrieve_rows()
        for row in rows:
            (
                transaction,
                amount,
            ) = self.resmap_ops.scrape.retrieve_transaction_and_amount(row)

            if operation == "allocate_all":
                self.ledger_functions.allocate_all_credits(
                    amount, self.webdriver.return_last_element(transaction)
                )

            if operation == "credit_all_charges":
                self.ledger_functions.credit_all_charges(is_concession)

            if operation == "delete_all_charges":
                try:
                    self.ledger_functions.delete_charges(transaction)
                except:
                    pass

            if operation == "delete_all_late_fees":
                if "late" in transaction or transaction in "late":
                    self.ledger_functions.delete_charges("Late")


class LedgerFunctions:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.credit_ops = CreditOps(webdriver)

    def delete_charges(self, transaction):
        self.webdriver.click_element(self.webdriver.return_last_element(transaction))
        self.transaction_ops.delete_charge()

    def allocate_all_credits(self, amount, element):
        if amount.startswith("(") or amount.endswith(")"):
            self.webdriver.click_element(element)
            self.transaction_ops.auto_allocate()

    def credit_all_charges(self, is_concession):
        self.webdriver.click_element(self.webdriver.return_last_element("Add Credit"))
        self.credit_ops.credit_charge(is_concession)
