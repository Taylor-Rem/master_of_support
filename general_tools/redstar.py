from selenium.webdriver.common.by import By
from os_tools.os_interact import OSInteract
from ledger_tools.ledger_interact import LedgerInteract


class Redstar:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.os_interact = OSInteract
        ledger_interact = LedgerInteract(webdriver)

        file_path = self.os_interact.retrieve_file("redstar_report")
        URLs = self.os_interact.csv_ops.get_url_columns(file_path)

        self.auto_redstar = AutoRedstar(webdriver, ledger_interact, URLs)
        self.redstar_ops = RedstarOps(webdriver, ledger_interact, URLs)

    def run_auto_redstar(self):
        self.auto_redstar.loop_through_ledgers()

    def run_redstar_ops(self):
        self.redstar_ops.open_ledger()


class AutoRedstar:
    def __init__(self, webdriver, URLs):
        self.webdriver = webdriver
        self.URLs = URLs

    def loop_through_ledgers(self):
        for URL in self.URLs:
            if not self.webdriver.element_status(By.XPATH, '//td//font[@color="red"]'):
                continue
            self.webdriver.driver.get(URL)


class RedstarOps:
    def __init__(self, webdriver, URLs):
        self.webdriver = webdriver
        self.URLs = URLs
        self.count = 0

    def open_ledger(self):
        self.webdriver.driver.get(self.URLs[self.count])

    def cycle_ledger(self, next):
        if next:
            self.count += 1
        else:
            self.count -= 1
        self.open_ledger()
