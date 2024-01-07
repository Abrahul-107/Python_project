import mysql.connector
from decimal import Decimal


# Custom exception for account number
class AccountNotFoundException(Exception):
    pass
# Custom exception for insufficient funds
class InsufficientFundsException(Exception):
    pass


class Bank:
    def __init__(self):
        self._db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Mysql@107",
            auth_plugin='Mysql@107',
            database='bankmanagementsystem'
        )
        self._db_cursor = self._db_connection.cursor()

    def __del__(self):
        if self._db_connection.is_connected():
            self._db_cursor.close()
            self._db_connection.close()
        
    # Checks if an account exists based on the provided account_number.
    def _account_exists(self, account_number):
        check_query = "SELECT COUNT(*) FROM accountdetails WHERE account_number = %s"
        values = (account_number,)

        try:
            self._db_cursor.execute(check_query, values)
            count = self._db_cursor.fetchone()[0]
            return count > 0
        except mysql.connector.Error as err:
            print(f"Error checking account existence: {err}")
            return False



    # Retrieves account details based on the provided account_number.
    def _get_account(self, account_number):
        try:
            # Fetch account details from the database
            select_query = "SELECT * FROM accountdetails WHERE account_number = %s"
            self._db_cursor.execute(select_query, (account_number,))
            account_data = self._db_cursor.fetchone()

            if account_data:
                return {
                    'account_number': account_data[1],
                    'name': account_data[2],
                    'transaction_type': account_data[3],
                    'initial_balance': account_data[4],
                    'transaction_date': account_data[5]
                }
            else:
                raise AccountNotFoundException("Account not found. Please enter a valid account number.")
        except mysql.connector.Error as err:
            print(f"Error retrieving account details: {err}")


    def _log_transaction(self, account_number, transaction_type, amount):
        log_query = """
        INSERT INTO transaction_history (account_number, transaction_type, amount)
        VALUES (%s, %s, %s)
        """
        values = (account_number, transaction_type, amount)

        try:
            self._db_cursor.execute(log_query, values)
            self._db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error logging transaction: {err}")
            self._db_connection.rollback()


        


    # Creates a new account with the specified account_number, name, and optional initial_balance.
    # If the account_number already exists, it notifies the user about the duplication.
    def create_account(self, account_number, name, initial_balance=0):
        try:
            account_query = "SELECT * FROM accountdetails WHERE account_number = %s"
            self._db_cursor.execute(account_query, (account_number,))
            existing_account = self._db_cursor.fetchone()

            if existing_account:
                update_query = "UPDATE accountdetails SET initial_balance = %s WHERE account_number = %s"
                self._db_cursor.execute(update_query, (initial_balance, account_number))
                self._db_connection.commit()
                print(f"Account already exists. Updated balance: {initial_balance}")
            else:
                insert_query = "INSERT INTO accountdetails (account_number, name, transaction_type, initial_balance) VALUES (%s, %s, %s, %s)"
                self._db_cursor.execute(insert_query, (account_number, name, 'CREATE', initial_balance))
                self._db_connection.commit()
                print("Congratulations! Your account is created successfully.")
        except mysql.connector.Error as e:
            print(f"Error: {e}")



            
    # Deposits a specified amount into the account associated with the provided account_number.
    def deposit(self, account_number, amount):
        try:
            account = self._get_account(account_number)

            new_balance = account['initial_balance'] + Decimal(amount)

            update_query = "UPDATE accountdetails SET initial_balance = %s WHERE account_number = %s"
            self._db_cursor.execute(update_query, (new_balance, account_number))
            self._db_connection.commit()

            print(f"Deposit successful. New Balance is: {new_balance}")
            self._log_transaction(account_number, 'DEPOSIT', amount)
        except (AccountNotFoundException, mysql.connector.Error) as e:
            print(f"Error: {e}")


    # Validates if a transfer between sender and receiver accounts with the given amount is feasible.
    def _validate_transfer(self, sender_account, receiver_account, amount):
        try:
            # Fetch sender details
            sender_query = "SELECT * FROM accountdetails WHERE account_number = %s"
            self._db_cursor.execute(sender_query, (sender_account,))
            sender = self._db_cursor.fetchone()

            # Fetch receiver details
            receiver_query = "SELECT * FROM accountdetails WHERE account_number = %s"
            self._db_cursor.execute(receiver_query, (receiver_account,))
            receiver = self._db_cursor.fetchone()

            if sender and receiver:
                if Decimal(sender[4]) >= Decimal(amount):  # Assuming initial_balance is at index 4
                    # Update sender's balance
                    sender_balance = Decimal(sender[4]) - Decimal(amount)
                    update_sender_query = "UPDATE accountdetails SET initial_balance = %s WHERE account_number = %s"
                    self._db_cursor.execute(update_sender_query, (sender_balance, sender_account))

                    # Update receiver's balance
                    receiver_balance = Decimal(receiver[4]) + Decimal(amount)
                    update_receiver_query = "UPDATE accountdetails SET initial_balance = %s WHERE account_number = %s"
                    self._db_cursor.execute(update_receiver_query, (receiver_balance, receiver_account))

                    self._db_connection.commit()

                    return True
                else:
                    raise InsufficientFundsException("Insufficient funds for this transfer")
            else:
                raise AccountNotFoundException("Account not found. Please enter valid account numbers.")
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return False




           
    # Withdraws a specified amount from the account associated with the provided account_number.
    def withdraw(self, account_number, amount):
        try:
            account = self._get_account(account_number)

            if account['initial_balance'] >= Decimal(amount):
                new_balance = account['initial_balance'] - Decimal(amount)
                update_query = "UPDATE accountdetails SET initial_balance = %s WHERE account_number = %s"
                self._db_cursor.execute(update_query, (new_balance, account_number))
                self._db_connection.commit()

                print(f"Withdrawal successful. Your new balance is: {new_balance}")
                self._log_transaction(account_number, 'WITHDRAW', amount)
            else:
                raise InsufficientFundsException("Insufficient funds")
        except (AccountNotFoundException, InsufficientFundsException, mysql.connector.Error) as e:
            print(f"Error: {e}")
    

    # Retrieves and displays the current balance of the account associated with the provided account_number.
    def check_balance(self, account_number):
        try:
            # Fetch account details
            account_query = "SELECT * FROM accountdetails WHERE account_number = %s"
            self._db_cursor.execute(account_query, (account_number,))
            account = self._db_cursor.fetchone()

            if account:
                print(f"Your balance is: {account[4]}")  # Assuming initial_balance is at index 4
            else:
                raise AccountNotFoundException("Account not found. Please enter a valid account number.")
        except mysql.connector.Error as e:
            print(f"Error: {e}")


    # Transfers a specified amount from the sender's account to the receiver's account.
    def send_money(self, sender_account, receiver_account, amount):
        try:
            if self._validate_transfer(sender_account, receiver_account, amount):
                print(f"Money sent successfully from Ac No: {sender_account} to Ac no: {receiver_account}")
                self._log_transaction(sender_account, 'TRANSFER_SEND', amount)
                self._log_transaction(receiver_account, 'TRANSFER_RECEIVE', amount)
        except (AccountNotFoundException, InsufficientFundsException) as e:
            print(f"Error: {e}")

    
    def view_profile(self,account_number):
        try:
            select_query = "SELECT * FROM accountdetails WHERE account_number = %s"
            self._db_cursor.execute(select_query, (account_number,))
            account_data = self._db_cursor.fetchone()

            if account_data:
                print("Account Details:")
                print(f"Account Number: {account_data[1]}")
                print(f"Name: {account_data[2]}")
                print(f"Balance: {account_data[4]}")
            else:
                raise AccountNotFoundException("Account not found. Please enter a valid account number.")
        except mysql.connector.Error as err:
            print(f"Error retrieving account details: {err}")

    def transaction_history(self, account_number):
        try:
            view_query ="SELECT * FROM transaction_history WHERE account_number = %s ORDER BY transaction_date DESC"

            self._db_cursor.execute(view_query, (account_number,))  # Note the comma to make it a tuple
            account_data = self._db_cursor.fetchall()

            if account_data:
                print(f" Transaction History for {account_number}")
                for transaction in account_data:
                    print(f"\n Account Number: {transaction[1]} \n Transaction Type: {transaction[2]} \n Amount: {transaction[3]} \n Transaction Date & Time : {transaction[4]}")
            else:
                raise AccountNotFoundException("Account not found. Please enter a valid account number.")
        except mysql.connector.Error as err:
            print(f"Error retrieving transaction details: {err}")


