import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont

import backend

class BankingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Online Banking System')
        self.setGeometry(100, 100, 400, 300)

        self.label_account = QLabel('Account Number:', self)
        self.input_account = QLineEdit(self)
        self.label_pin = QLabel('PIN:', self)
        self.input_pin = QLineEdit(self)
        self.input_pin.setEchoMode(QLineEdit.Password)
        self.button_login = QPushButton('Login', self)
        self.button_login.clicked.connect(self.login)

        self.label_transaction = QLabel('', self)
        self.input_recipient = QLineEdit(self)
        self.label_recipient = QLabel('Recipient Account Number:', self)
        self.input_amount = QLineEdit(self)
        self.label_amount = QLabel('Amount:', self)
        self.button_deposit = QPushButton('Deposit', self)
        self.button_deposit.clicked.connect(self.deposit)
        self.button_withdraw = QPushButton('Withdraw', self)
        self.button_withdraw.clicked.connect(self.withdraw)
        self.button_transfer = QPushButton('Transfer', self)
        self.button_transfer.clicked.connect(self.transfer)
        self.button_check_balance = QPushButton('Check Balance', self)
        self.button_check_balance.clicked.connect(self.check_balance)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_account)
        vbox.addWidget(self.input_account)
        vbox.addWidget(self.label_pin)
        vbox.addWidget(self.input_pin)
        vbox.addWidget(self.button_login)

        vbox.addWidget(self.label_transaction)
        vbox.addWidget(self.label_recipient)
        vbox.addWidget(self.input_recipient)
        vbox.addWidget(self.label_amount)
        vbox.addWidget(self.input_amount)
        vbox.addWidget(self.button_deposit)
        vbox.addWidget(self.button_withdraw)
        vbox.addWidget(self.button_transfer)
        vbox.addWidget(self.button_check_balance)

        self.setLayout(vbox)

        self.applyStyles()

    def applyStyles(self):
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)

        labels = [self.label_account, self.label_pin, self.label_recipient, self.label_amount]
        for label in labels:
            label.setFont(font)

        buttons = [self.button_login, self.button_deposit, self.button_withdraw, self.button_transfer, self.button_check_balance]
        for button in buttons:
            button.setStyleSheet("background-color: #4CAF50; color: white;")
            button.setFont(font)

        inputs = [self.input_account, self.input_pin, self.input_recipient, self.input_amount]
        for input_field in inputs:
            input_field.setStyleSheet("background-color: #f2f2f2;")

        self.label_transaction.setStyleSheet("color: #1a1a1a; font-weight: bold;")

    def login(self):
        account_num = int(self.input_account.text())
        pin = int(self.input_pin.text())

        user_account = backend.authenticate(account_num, pin)
        if user_account:
            self.user_account = user_account
            self.showMainScreen()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid account number or PIN.')

    def showMainScreen(self):
        self.label_transaction.setText(f"Welcome, {self.user_account.name}! Balance: {self.user_account.balance}")

    def deposit(self):
        amount = int(self.input_amount.text())
        if amount > 0:
            if self.user_account.deposit(amount):
                self.label_transaction.setText(f"Deposit successful. New balance: {self.user_account.balance}")
            else:
                self.label_transaction.setText("Invalid deposit amount")
        else:
            self.label_transaction.setText("Invalid deposit amount")

    def withdraw(self):
        amount = int(self.input_amount.text())
        if amount > 0:
            if self.user_account.withdraw(amount):
                self.label_transaction.setText(f"Withdrawal successful. New balance: {self.user_account.balance}")
            else:
                self.label_transaction.setText("Insufficient funds or invalid withdrawal amount")
        else:
            self.label_transaction.setText("Invalid withdrawal amount")

    def transfer(self):
        recipient_account_num = int(self.input_recipient.text())
        amount = int(self.input_amount.text())
        if backend.transfer_funds(self.user_account.account_num, recipient_account_num, amount):
            self.label_transaction.setText(f"Transfer successful. New balance: {self.user_account.balance}")
        else:
            self.label_transaction.setText("Transfer failed. Check recipient account or insufficient funds")

    def check_balance(self):
        balance = self.user_account.balance
        self.label_transaction.setText(f"Your current balance: {balance}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    banking_app = BankingApp()
    banking_app.show()
    sys.exit(app.exec_())
