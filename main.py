from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QStackedWidget,
)
from os_interact import OSInteract
from csv_ops import CsvOperations
from webdriver_ops import WebdriverOperations
from open_tickets import OpenTickets
from redstar import RunRedstar
from scrape import Scrape
from resmap_ops import ResmapOperations


class App(QWidget):
    def __init__(self):
        super().__init__()
        # Create stacked widget
        self.stack = QStackedWidget()

        # Init Classes
        self.webdriver = WebdriverOperations()
        self.os_interact = OSInteract()
        self.csv_ops = CsvOperations()
        self.scrape = Scrape(self.webdriver)
        self.resmap_ops = ResmapOperations(self.webdriver, self.scrape)

        # Init UI
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Support Deez")

        self.init_windows()
        self.add_widgets()

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stack)

    def init_windows(self):
        self.init_main_window()
        self.ticket_helper = TicketHelper(self)
        self.redstar = Redstar(self)

    def add_widgets(self):
        self.stack.addWidget(self.main_window)
        self.stack.addWidget(self.ticket_helper)
        self.stack.addWidget(self.redstar)

    def init_main_window(self):
        self.main_window = QWidget()
        main_layout = QVBoxLayout()
        self.main_window.setLayout(main_layout)
        self.create_button("Ticket Master", self.switch_to_ticket, main_layout)
        self.create_button("Choose Report", self.switch_to_report, main_layout)
        self.create_button("Redstar Master", self.switch_to_redstar, main_layout)
        self.create_button("Quit App", self.quit_app, main_layout)

    def create_button(self, text, callback, layout):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        layout.addWidget(button)

    def switch_to_ticket(self):
        self.stack.setCurrentWidget(self.ticket_helper)
        self.webdriver.open_program(self.webdriver.manage_portal_url)

    def switch_to_report(self):
        print("Report Master")

    def switch_to_redstar(self):
        self.stack.setCurrentWidget(self.redstar)
        self.webdriver.open_program(self.webdriver.res_map_url)

    def quit_app(self):
        self.close()


class HelperWidget(QWidget):
    def __init__(self, main_app, title):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel(title, self)

    def create_button(self, text, callback):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        self.layout.addWidget(button)
        return button

    def go_back(self):
        self.main_app.stack.setCurrentWidget(self.main_app.main_window)

    def add_back_btn(self):
        self.back_btn = self.create_button("Back", self.go_back)


class TicketHelper(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Ticket Helper")
        self.open_btn = self.create_button("Open Ticket", self.open_ticket)
        self.add_back_btn()
        self.open_ticket = OpenTickets(
            main_app.webdriver, main_app.scrape, main_app.resmap_ops
        )

    def open_ticket(self):
        self.open_ticket.open_ticket()


class Redstar(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Red Star")
        self.redstar = RunRedstar(
            main_app.webdriver, main_app.os_interact, main_app.csv_ops, main_app.scrape
        )
        self.run_report = self.create_button("Run Report", self.run_report)
        self.add_back_btn()

    def run_report(self):
        self.redstar.run_redstar()


if __name__ == "__main__":
    OSInteract().create_folders()
    app = QApplication([])
    main_app = App()
    main_app.show()
    app.exec_()
