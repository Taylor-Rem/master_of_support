from PyQt5.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
)
from os_tools.os_interact import OSInteract
from webdriver_ops import WebdriverOperations

from resmap_tools.webpage_ops import ResmapOperations, ManageportalOps

from .frontend_subclasses import (
    TicketHelper,
    TicketOps,
    ChooseReport,
    ReportHelper,
    RedstarWindow,
    RedstarHelper,
)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.stack = QStackedWidget()
        self.previous_widgets = []

        self.init_classes()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Support Deez")

        self.init_windows()
        self.add_widgets()

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stack)

    def init_classes(self):
        self.webdriver = WebdriverOperations()
        self.os_interact = OSInteract()
        self.resmap_ops = ResmapOperations(self.webdriver)
        self.manageportal_ops = ManageportalOps(self.webdriver)

    def init_windows(self):
        self.ticket_helper = TicketHelper(self)
        self.ticket_ops = TicketOps(self)
        self.choose_report = ChooseReport(self)
        self.report_helper = ReportHelper(self)
        self.redstar_window = RedstarWindow(self)
        self.redstar_helper = RedstarHelper(self)
        self.init_main_window()

    def add_widgets(self):
        windows = [
            self.main_window,
            self.ticket_helper,
            self.ticket_ops,
            self.choose_report,
            self.report_helper,
            self.redstar_window,
            self.redstar_helper,
        ]
        for window in windows:
            self.stack.addWidget(window)

    def init_main_window(self):
        self.main_window = QWidget()
        main_layout = QVBoxLayout()
        self.main_window.setLayout(main_layout)

        button_configs = [
            {
                "name": "Ticket Master",
                "method": lambda: self.switch_window(
                    self.ticket_helper, self.webdriver.manage_portal_url
                ),
            },
            {
                "name": "Choose Report",
                "method": lambda: self.switch_window(
                    self.choose_report, self.webdriver.res_map_url
                ),
            },
            {
                "name": "Redstar Master",
                "method": lambda: self.switch_window(
                    self.redstar_window, self.webdriver.res_map_url
                ),
            },
        ]

        for config in button_configs:
            self.create_button(config["name"], config["method"], main_layout)

    def create_button(self, text, callback, layout):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        layout.addWidget(button)

    def switch_window(self, window, open_program=None):
        self.previous_widgets.append(self.stack.currentWidget())
        self.stack.setCurrentWidget(window)
        if open_program:
            self.webdriver.switch_to_primary_tab()
            self.webdriver.open_program(open_program)

    def quit_app(self):
        self.close()
