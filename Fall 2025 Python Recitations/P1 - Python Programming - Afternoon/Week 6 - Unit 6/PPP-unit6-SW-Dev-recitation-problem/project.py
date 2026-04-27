'''
Task - 1: Debug the code
# 1. use print statements 
# 2. use try except clause -- application crash error
# 3. Use debugger -- logical error

Task-2: refactor this code to 4 python classes
create a folder bank app and put files 
* bank.py
* accounts.py
* errors.py
* in outer folder maintain main.py

Task-3: 
* Add exception Handling
* Account Not found
* Insufficient Funds
* Invalid Amount
* Duplicate Account error

Task-4
* Add testing - pytest
'''

#A bank transaction app
# Account Class
class Account:
    def __init__(self, account_number, account_holder, balance=0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount} to {self.account_holder}'s account.")

    def withdraw(self, amount):
        self.balance -= amount
        print(f"Withdrew {amount} from {self.account_holder}'s account.")

    def get_balance(self):
        return self.balance

    def display(self):
        print(f"Account: {self.account_number}, Holder: {self.account_holder}, Balance: {self.balance}")


# Bank Class
class Bank:
    def __init__(self):
        self.customers = {}
        self.accounts = {}

    def create_account(self, account_number, account_holder):
        account = Account(account_number, account_holder)
        self.accounts[account_number] = account
        self.customers[account_holder] = account_number
        print(f"Created account for {account_holder}.")

    def deposit(self, account_number, amount):
        account = self.accounts[account_number]
        account.deposit(amount)

    def withdraw(self, account_number, amount):
        account = self.accounts[account_number]
        account.withdraw(amount)

    def display_account(self, account_number):
        account = self.accounts[account_number]
        account.display()

    def get_account_balance(self, account_number):
        account = self.accounts[account_number]
        return account.get_balance()


# Example usage of the Bank system

if __name__ == "__main__":
    bank = Bank()
    
    # Creating accounts
    bank.create_account(1001, "Alice")
    bank.create_account(1002, "Bob")
    
    # Performing some transactions
    bank.deposit(1001, 500)
    bank.deposit(1001, '500')
    bank.withdraw(1001, 200)
    
    bank.deposit(1002, 1000)
    bank.withdraw(1002, 1200)  # This will make the balance negative (no validation)

    # Display accounts
    bank.display_account(1001)
    bank.display_account(1002)
    
    # Check balances
    print("Alice's Balance:", bank.get_account_balance(1001))
    print("Bob's Balance:", bank.get_account_balance(1002))

