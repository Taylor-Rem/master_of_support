from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class RunRedstar:
    def __init__(self, webdriver, os_interact, csv_ops, scrape):
        self.webdriver = webdriver
        self.os_interact = os_interact
        self.csv_ops = csv_ops
        self.scrape = scrape

    def run_redstar(self):
        file_path = self.os_interact.retrieve_file("redstar_report")
        URLs = self.csv_ops.get_url_columns(file_path)
        for URL in URLs:
            self.webdriver.driver.get(URL)
            if self.redstar_status:
                self.loop_through_table

    def redstar_status(self):
        try:
            element = self.webdriver.driver.find_element(
                By.XPATH,
                '//font[@color="red"]/ancestor::td[@class="td1" or @class="td2"]',
            )
            return True
        except NoSuchElementException:
            return False

    def loop_through_table(self, table, rows, table_num):
        link = None
