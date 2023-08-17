from selenium.webdriver.common.by import By


class LedgerInteract:
    def __init__(self, webdriver, resmap_ops):
        self.webdriver = webdriver
        self.resmap_ops = resmap_ops

    def current_month(self, operation, is_concession=False):
        rows = self.resmap_ops.get_rows(
            By.XPATH,
            self.resmap_ops.scrape.choose_table(
                self.resmap_ops.scrape.tables["current_month"]
            ),
        )
        for row in rows:
            (
                transaction,
                amount,
            ) = self.resmap_ops.scrape.retrieve_transaction_and_amount(row)

            if operation == "allocate_all":
                self.resmap_ops.allocate_all_credits(
                    amount, self.webdriver.return_last_element(transaction)
                )

            if operation == "credit_all_charges":
                self.resmap_ops.credit_all_charges(is_concession)

            if operation == "delete_all_charges":
                self.resmap_ops.delete_charges(transaction)

            if operation == "delete_all_late_fees":
                if "Late" in transaction:
                    self.resmap_ops.delete_charges("Late")

    def delete_charges(self, transaction):
        self.webdriver.click_element(self.webdriver.return_last_element(transaction))
        self.webdriver.click(By.NAME, "delete")
        alert = self.webdriver.driver.switch_to.alert
        alert.accept()

    def allocate_all_credits(self, amount, element):
        if amount.startswith("(") or amount.endswith(")"):
            self.webdriver.click_element(element)
            self.transaction_ops.auto_allocate()

    def credit_all_charges(self, is_concession=False):
        self.webdriver.click_element(self.webdriver.return_last_element("Add Credit"))
        rows = self.get_rows(By.XPATH, "//tr[contains(@class, 'td')]")
        row = rows[-1]
        columns = row.find_all("td")
        name = columns[0].text.strip()
        bill_amount_str = columns[2].text.strip()
        bill_amount_replace = bill_amount_str.replace("$", "").replace(" ", "")
        bill_amount = float(bill_amount_replace)
        select_element = self.webdriver.driver.find_element(
            By.XPATH, "//select[@name='ttid']"
        )
        select = Select(select_element)
        if (name == "Rent" or "Home Rental") and is_concession:
            select.select_by_visible_text(f"{name} Concession")
        else:
            select.select_by_visible_text(name)
        credit_input = self.webdriver.driver.find_element(
            By.XPATH, "//input[@type='text' and @name='amount']"
        )
        self.webdriver.send_keys_element(credit_input, bill_amount)
        comments = self.webdriver.driver.find_element(
            By.XPATH, "//textarea[@name='comments']"
        )
        self.webdriver.send_keys_element(comments, "charge concession")
        self.webdriver.click(By.XPATH, "//input[@type='submit' and @name='submit1']")
