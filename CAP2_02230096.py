import time

# The Customer class to hold basic customer details
class Customer:
    def __init__(self, name, age):
        self.name = name  # The customer's name
        self.age = age  # The customer's age

    def display_info(self):
        return f"Thank you, {self.name.title()}, {self.age} years old"  # Display customer's name and age

# The Account class, inheriting from Customer, to represent a bank account
class Account(Customer):
    total_deposits = 0  # Track overall deposits across all accounts
    total_withdrawals = 0  # Track overall withdrawals across all accounts

    def __init__(self, name, age, balance, account_num, passwd, acc_type):
        super().__init__(name, age)  # Initialize the parent Customer class
        self.balance = balance  # The account's balance
        self.account_num = account_num  # Unique account number
        self.passwd = passwd  # Account password
        self.acc_type = acc_type  # Account type (Personal/Commercial)

    def show_balance(self):
        return f"{self.name}, your current balance is: ${round(self.balance, 2)}"  # Display account balance

    def deposit_funds(self, amount):
        self.balance += amount  # Add the deposit amount to the balance
        Account.total_deposits += amount  # Update total deposits
        print("Deposit completed!")
        return f"Your updated balance is: ${round(self.balance, 2)}"  # Display updated balance

    def withdraw_funds(self, amount):
        if self.balance < amount:
            return "Withdrawal failed, insufficient balance."  # Insufficient funds message
        else:
            self.balance -= amount  # Deduct the withdrawal amount from the balance
            Account.total_withdrawals += amount  # Update total withdrawals
            print("Withdrawal completed!")
            return f"Your updated balance is: ${round(self.balance, 2)}"  # Display updated balance

    def save_details(self, filename='accounts.txt'):
        # Save account details to a file
        acc_info = f"{self.name},{self.age},{self.account_num},{self.passwd},{self.acc_type},{self.balance}\n"
        with open(filename, 'a') as file:
            file.write(acc_info)

    def transfer_funds(self, recipient, amount):
        if self.balance < amount:
            return "Transfer failed, insufficient funds."  # Insufficient funds message
        else:
            self.balance -= amount  # Deduct the transfer amount from the sender's balance
            recipient.balance += amount  # Add the transfer amount to the recipient's balance
            print(f"Successfully transferred ${amount} to {recipient.name}.")
            return f"Your updated balance is: ${round(self.balance, 2)}"  # Display updated balance

# Function to load all accounts from a file
def load_all_accounts(filename='accounts.txt'):
    accounts = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                name, age, acc_num, pwd, acc_type, balance = line.strip().split(',')
                accounts.append(Account(name, int(age), float(balance), acc_num, pwd, acc_type))
    except FileNotFoundError:
        pass  # If the file does not exist, return an empty list
    return accounts

# Function to load an account from a file using account number and password
def load_account(account_num, passwd, accounts):
    for account in accounts:
        if account.account_num == account_num and account.passwd == passwd:
            print("Login successful.")
            return account
    print("Invalid account number or password.")
    return None

# Function to generate a unique account number
def generate_account_num():
    current_time = str(int(time.time() * 1000))
    return current_time[-8:]

# Function to present user options and handle their choices
def customer_options(account, all_accounts):
    print('Account created successfully.')
    print("Please select an option by entering the corresponding number:")
    while True:
        choice = int(input("1) Check Balance\n2) Withdraw\n3) Deposit\n4) View Total Deposits\n5) View Total Withdrawals\n6) Transfer\n7) Logout\nEnter choice: "))
        if choice == 1:
            print(account.show_balance())  # Show account balance
        elif choice == 2:
            amount = float(input(f"{account.name.title()}, enter the amount to withdraw: "))
            print(account.withdraw_funds(amount))  # Withdraw funds
        elif choice == 3:
            amount = float(input(f"{account.name.title()}, enter the amount to deposit: "))
            print(account.deposit_funds(amount))  # Deposit funds
        elif choice == 4:
            print(f"Total deposits across all accounts: ${Account.total_deposits}")  # Display total deposits
        elif choice == 5:
            print(f"Total withdrawals across all accounts: ${Account.total_withdrawals}")  # Display total withdrawals
        elif choice == 6:
            recipient_num = input("Enter the recipient's account number: ")
            recipient = next((acc for acc in all_accounts if acc.account_num == recipient_num), None)
            if recipient:
                amount = float(input(f"Enter the amount to transfer to {recipient.name}: "))
                print(account.transfer_funds(recipient, amount))  # Transfer funds
            else:
                print("Recipient account not found.")
        elif choice == 7:
            print("Thank you for using Karma Bank. Goodbye!")
            # Save the updated account details to file
            with open('accounts.txt', 'w') as file:
                for acc in all_accounts:
                    acc_info = f"{acc.name},{acc.age},{acc.account_num},{acc.passwd},{acc.acc_type},{acc.balance}\n"
                    file.write(acc_info)
            return True  # Logout
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

# Function to create a new bank account using user input
def create_new_account():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    account_num = generate_account_num()  # Generate a unique account number
    passwd = input("Create a password: ")
    acc_type = input("Enter account type (Personal/Commercial): ")
    balance = float(input("Enter your initial deposit amount: "))
    new_account = Account(name, age, balance, account_num, passwd, acc_type)
    new_account.save_details()  # Save the account details to a file
    return new_account

# Main function to run the banking system
def main():
    all_accounts = load_all_accounts()  # Load all accounts from file
    while True:
        print("Welcome to Karma Bank")
        choice = input("1) Create Account\n2) Login\n3) Exit\nEnter choice: ")

        if choice == '1':
            new_account = create_new_account()
            all_accounts.append(new_account)  # Add the new account to the list
            print(f"Account created successfully. Account Number: {new_account.account_num}, Password: {new_account.passwd}")
            customer_options(new_account, all_accounts)  # Present user options
        elif choice == '2':
            account_num = input("Enter your account number: ")
            passwd = input("Enter your password: ")
            existing_account = load_account(account_num, passwd, all_accounts)
            if existing_account:
                customer_options(existing_account, all_accounts)  # Present user options
        elif choice == '3':
            print("Thank you for visiting Karma Bank. Have a great day!")
            break  # Exit the program
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
