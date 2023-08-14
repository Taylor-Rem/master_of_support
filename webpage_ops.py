from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


class ResmapOperations:
    def __init__(self, webdriver, scrape):
        self.webdriver = webdriver
        self.scrape = scrape
        self.tables = {"previous_month": -5, "current_month": -4, "bottom": -1}

    def open_ledger(self, property, unit, resident):
        self.open_property(property)
        if unit is not None:
            self.open_unit_and_ledger(unit, resident)

    def open_property(self, property):
        self.webdriver.click(By.XPATH, "//a[contains(., 'CHANGE PROPERTY')]")
        self.webdriver.click(By.XPATH, f"//a[contains(., '{property}')]")

    def open_unit(self, unit):
        self.webdriver.send_keys(By.NAME, "search_input", unit + Keys.ENTER)

    def click_ledger(self):
        self.webdriver.click(By.XPATH, ".//a[text()='Ledger']")

    def search_resident(self, resident, num):
        self.webdriver.click(
            By.ID,
            f"former{num}",
        )
        self.webdriver.send_keys(By.NAME, "ressearch", resident + Keys.ENTER)

    def compare_resident(self, resident):
        RM_resident = self.scrape.scrape_resident()
        if RM_resident and resident:
            if resident in RM_resident or RM_resident in resident:
                return True
            else:
                return False
        return False

    def open_unit_and_ledger(self, unit, resident):
        self.open_unit(unit)
        if self.compare_resident(resident) or resident is None:
            self.click_ledger()
        else:
            self.open_former_ledger(unit, resident)

    def search_resident_and_open_ledger(self, resident):
        try:
            self.search_resident(resident, 1)
            self.click_ledger()
        except NoSuchElementException:
            self.search_resident(resident, 2)
            self.click_ledger()
        except:
            print(f"there was a problem with ledger {resident}")
            pass

    def open_former_ledger(self, unit, resident):
        try:
            self.webdriver.click(By.XPATH, f".//a[text()='{unit}']")
            self.webdriver.click(
                By.XPATH,
                "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[2]/td[5]/a",
            )
            self.click_last_ledger()
        except NoSuchElementException:
            self.search_resident_and_open_ledger(resident)

    def click_last_ledger(self):
        table = self.webdriver.driver.find_element(
            By.XPATH,
            "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody",
        )
        ledger_links = table.find_elements(By.XPATH, ".//a[text()='Ledger']")
        if ledger_links:
            self.webdriver.click_element(ledger_links[-1])
        else:
            self.click_ledger()

    def is_header_row(self, row):
        return row.find("td", class_="th3") is not None

    def choose_table(self, num):
        return f"/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[last(){num}]/tbody/tr[2]/td/table/tbody"

    def define_table(self, table_num):
        table_elements = self.webdriver.driver.find_elements(
            By.XPATH, self.choose_table(table_num)
        )
        table = table_elements[0] if table_elements else None
        return table

    def get_rows(self, table_num):
        table = self.define_table(table_num)
        if table:
            soup = BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
            rows = soup.find_all("tr")
            return rows
        else:
            return None

    def retrieve_transaction_and_amount(self, row):
        cells = row.find_all("td")
        transaction = cells[2].get_text(strip=True)
        amount = cells[3].get_text(strip=True)
        return transaction, amount


class ManageportalOps:
    def __init__(self, webdriver):
        self.webdriver = webdriver

    def resolve_ticket(self, icon, back):
        self.webdriver.click(By.XPATH, "//button[contains(., 'Change Ticket Status')]")

        self.click_button("button", icon)

        if back:
            self.click_button("a", back)

    def click_button(self, element_type, icon):
        xpath = f"//{element_type}[.//i[contains(@class, 'material-icons') and text()='{icon}']]"
        self.webdriver.wait_click(By.XPATH, xpath)
        self.webdriver.click(By.XPATH, xpath)
