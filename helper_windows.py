from PyQt5.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QMessageBox,
    QInputDialog,
)

from ledger_interact import LedgerInteract

from functools import partial


class HelperWidget(QWidget):
    def __init__(self, main_app, title):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle(title)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(title, self)
        self.layout.addWidget(self.label)

        self.button_layout = QVBoxLayout()
        self.layout.addLayout(self.button_layout)

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


class LedgerOps(HelperWidget):
    def __init__(self, main_app, title):
        super().__init__(main_app, title)
        self.ledger_interact = LedgerInteract(main_app.webdriver, main_app.resmap_ops)

    def create_ledger_buttons(self):
        self.allocate_all_btn = self.create_button(
            "Allocate All", partial(self.click_button, "allocate_all")
        )
        self.credit_all_charges_btn = self.create_button(
            "Credit All Charges", partial(self.click_button, "credit_all_charges")
        )
        self.delete_all_charges_btn = self.create_button(
            "Delete All Charges", partial(self.click_button, "delete_all_charges")
        )
        self.delete_all_late_fees_btn = self.create_button(
            "Delete All Late Fees", partial(self.click_button, "delete_all_late_fees")
        )
        self.add_back_btn()

    def click_button(self, operation):
        if operation == "credit_all_charges":
            items = ["Concession", "Credit"]
            item, ok = QInputDialog.getItem(
                self, "Choose credit type", "Type:", items, 0, False
            )
            if ok and item:
                is_concession = item == "Concession"
                self.ledger_interact.current_month(operation, is_concession)
            else:
                QMessageBox.information(
                    self, "Operation canceled", "Credit operation was canceled."
                )
                return
        else:
            self.ledger_interact.current_month(operation)
