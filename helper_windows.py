from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel

from tickets import OpenTickets, TicketLedgerOps
from redstar import RunRedstar
from os_interact import OSInteract


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
        if self.main_app.previous_widgets:
            last_widget = self.main_app.previous_widgets.pop()
            self.main_app.stack.setCurrentWidget(last_widget)
        else:
            # In case the widget history is empty, fall back to the main window
            self.main_app.stack.setCurrentWidget(self.main_app.main_window)

    def add_back_btn(self):
        self.back_btn = self.create_button("⬅️ Back", self.go_back)


class TicketHelper(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Ticket Helper")
        self.icons = {
            "In Progress": "scatter_plot",
            "Resolved": "done_outline",
            "Back": "arrow_back",
        }

        self.open_btn = self.create_button("🤖 Open Ticket", self.open_ticket)
        self.in_progress_btn = self.create_button(
            "🔵 In Progress",
            lambda: self.change_ticket_status(
                self.icons["In Progress"], self.icons["⬅️Back"]
            ),
        )
        self.resolve_btn = self.create_button(
            "✅ Resolve", lambda: self.change_ticket_status(self.icons["Resolved"])
        )
        self.add_back_btn()
        self.open_ticket_op = OpenTickets(
            main_app.webdriver, main_app.scrape, main_app.resmap_ops
        )
        self.ticket_ledger_ops = TicketLedgerOps(main_app.webdriver)

    def open_ticket(self):
        # self.main_app.switch_window(self.main_app.ticket_ops)
        self.open_ticket_op.open_ticket()

    def change_ticket_status(self, icon, back=None):
        self.ticket_ledger_ops.change_ticket_status(icon, back)


class TicketOps(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Ticket Ops")
        self.add_back_btn()


class ChooseReport(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Choose Report")
        self.zero_btn = self.create_button("Zero Report", self.open_report)
        self.double_btn = self.create_button("Double Report", self.open_report)
        self.moveout_btn = self.create_button("Moveout Report", self.open_report)
        self.add_back_btn()
        self.os_interact = OSInteract()

    def open_report(self):
        self.main_app.switch_window(self.main_app.report_helper)


class ReportHelper(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Report Helper")
        self.complete_btn = self.create_button("Add", self.add_report)
        self.skip_btn = self.create_button("Skip", self.skip_report)
        self.add_back_btn()

    def add_report(self):
        pass

    def skip_report(self):
        pass


class Redstar(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Red Star")
        self.redstar = RunRedstar(main_app.webdriver, main_app.os_interact)
        self.run_report_btn = self.create_button("Run Report", self.run_report)
        self.add_back_btn()

    def run_report(self):
        self.redstar.run_redstar()
