from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel

from tickets import OpenTickets, TicketLedgerOps
from redstar import RunRedstar
from report_ops import ReportOperations


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
                self.icons["In Progress"], self.icons["Back"]
            ),
        )
        self.resolve_btn = self.create_button(
            "✅ Resolve", lambda: self.change_ticket_status(self.icons["Resolved"])
        )
        self.add_back_btn()
        self.open_ticket_op = OpenTickets(
            main_app.webdriver, main_app.scrape, main_app.resmap_ops
        )
        self.ticket_ledger_ops = TicketLedgerOps(
            main_app.webdriver, main_app.resmap_ops
        )

    def open_ticket(self):
        self.main_app.switch_window(self.main_app.ticket_ops)
        self.open_ticket_op.open_ticket()

    def change_ticket_status(self, icon, back=None):
        self.ticket_ledger_ops.change_ticket_status(icon, back)


class TicketOps(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Ticket Ops")
        self.ticket_ledger_ops = TicketLedgerOps(
            main_app.webdriver, main_app.resmap_ops
        )
        self.credit_all_charges_btn = self.create_button(
            "Credit All Charges", self.credit_all_charges
        )
        self.delete_late_fees_btn = self.create_button(
            "Delete Late Fees", self.delete_late_fees
        )
        self.add_back_btn()

    def credit_all_charges(self):
        self.ticket_ledger_ops.credit_all_charges()

    def delete_late_fees(self):
        self.ticket_ledger_ops.delete_all_late_fees()


class ChooseReport(HelperWidget):
    def __init__(self, main_app, os_interact):
        super().__init__(main_app, "Choose Report")
        self.zero_btn = self.create_button(
            "Zero Report", lambda: self.open_report("zero_report")
        )
        self.double_btn = self.create_button(
            "Double Report", lambda: self.open_report("double_report")
        )
        self.moveout_btn = self.create_button(
            "Moveout Report", lambda: self.open_report("moveout_report")
        )
        self.add_back_btn()
        self.os_interact = os_interact

    def open_report(self, report):
        try:
            report_ops = ReportOperations(
                self.main_app.webdriver, self.main_app.resmap_ops, report
            )
            report_helper_window = ReportHelper(self.main_app, report_ops)
            self.main_app.stack.addWidget(report_helper_window)
            self.main_app.switch_window(report_helper_window)
        except:
            print("Report Complete!")


class ReportHelper(HelperWidget):
    def __init__(self, main_app, report_ops=None):
        self.report_ops = report_ops
        super().__init__(main_app, "Report Helper")
        self.complete_btn = self.create_button("Add", self.add_report)
        self.skip_btn = self.create_button("Skip", self.skip_report)
        self.add_back_btn()

    def add_report(self):
        try:
            self.report_ops.add_button()
        except:
            self.main_app.switch_window(self.main_app.choose_report)
            print("Report Complete!")

    def skip_report(self):
        self.report_ops.skip_button()


class Redstar(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Red Star")
        self.redstar = RunRedstar(
            main_app.webdriver, main_app.os_interact, main_app.resmap_ops
        )
        self.run_report_btn = self.create_button("Run Report", self.run_report)
        self.add_back_btn()

    def run_report(self):
        self.redstar.run_redstar()
