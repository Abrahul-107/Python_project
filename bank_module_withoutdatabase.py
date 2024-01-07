# Custom exception for account number
class AccountNotFoundException(Exception):
    pass

# Custom exception for insufficient funds
class InsufficientFundsException(Exception):
    pass

'''The Bank class represents a simple bank management system that allows users to create accounts,
 deposit and withdraw money, check balances, and send money between accounts.'''
class Bank:
    '''Attributes:: _accounts : dict
        A dictionary that stores account information where the account number is the key and the value
        is a dictionary containing 'name' (account holder's name) and 'balance' (account balance).'''
    
    # Initializes a Bank object with an empty dictionary of accounts.
    def __init__(self):
        self._accounts = {}
        
    # Checks if an account exists based on the provided account_number.
    def _account_exists(self, account_number):
        return account_number in self._accounts

    # Retrieves account details based on the provided account_number.
    def _get_account(self, account_number):
        if self._account_exists(account_number):
            return self._accounts[account_number]
        else:
            raise AccountNotFoundException("Account not found. Please enter a valid account number.")

    # Creates a new account with the specified account_number, name, and optional initial_balance.
    # If the account_number already exists, it notifies the user about the duplication.
    def create_account(self, account_number, name, initial_balance=0):
        if not self._account_exists(account_number):
            self._accounts[account_number] = {'name': name, 'balance': initial_balance}
            print("Congratulations! Your account is created successfully.")
        else:
            print("Sorry, this account number already exists. Try with another number.")
            
    # Validates if a transfer between sender and receiver accounts with the given amount is feasible.
    def _validate_transfer(self, sender, receiver, amount):
        if sender['balance'] >= amount:
            sender['balance'] -= amount
            receiver['balance'] += amount
            return True
        else:
            raise InsufficientFundsException("Insufficient funds for this transfer")
           
    # Deposits a specified amount into the account associated with the provided account_number.
    def deposit(self, account_number, amount):
        try:
            account = self._get_account(account_number)
            account['balance'] += amount
            print(f"Deposit successful. New Balance is: {account['balance']}")
        except AccountNotFoundException as e:
            print(f"Error: {e}")

    # Withdraws a specified amount from the account associated with the provided account_number.
    def withdraw(self, account_number, amount):
        try:
            account = self._get_account(account_number)
            if account['balance'] >= amount:
                account['balance'] -= amount
                print(f"Withdrawal successful. Your new balance is: {account['balance']}")
            else:
                raise InsufficientFundsException("Insufficient funds")
        except (AccountNotFoundException, InsufficientFundsException) as e:
            print(f"Error: {e}")

    # Retrieves and displays the current balance of the account associated with the provided account_number.
    def check_balance(self, account_number):
        try:
            account = self._get_account(account_number)
            print(f"Your balance is: {account['balance']}")
        except AccountNotFoundException as e:
            print(f"Error: {e}")

    # Transfers a specified amount from the sender's account to the receiver's account.
    def send_money(self, sender_account, receiver_account, amount):
        try:
            sender = self._get_account(sender_account)
            receiver = self._get_account(receiver_account)

            if self._validate_transfer(sender, receiver, amount):
                print(f"Money sent successfully from Ac No: {sender_account} to Ac no: {receiver_account}")
                print(f"Sender's new balance: {sender['balance']}")
        except (AccountNotFoundException, InsufficientFundsException) as e:
            print(f"Error: {e}")