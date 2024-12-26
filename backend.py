class BankAccount:
    def __init__(self, account_num, pin, name, initial_balance=500):
        self.account_num = account_num
        self.pin = pin
        self.name = name
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False

    def transfer_funds(self, recipient_account, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            recipient_account.balance += amount
            return True
        else:
            return False

# Dictionary to store user accounts (for demonstration purposes)
user_accounts = {
    1001: BankAccount(1001, 1234, "Saridha"),
    1002: BankAccount(1002, 5678, "Viji")
}

def authenticate(account_num, pin):
    if account_num in user_accounts:
        user_account = user_accounts[account_num]
        if user_account.pin == pin:
            return user_account
    return None

def transfer_funds(sender_account_num, recipient_account_num, amount):
    if sender_account_num in user_accounts and recipient_account_num in user_accounts:
        sender_account = user_accounts[sender_account_num]
        recipient_account = user_accounts[recipient_account_num]
        return sender_account.transfer_funds(recipient_account, amount)
    else:
        return False