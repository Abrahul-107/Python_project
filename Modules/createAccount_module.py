def createAccount(bank):
    while True:
        account_number = input("Enter account number: ")
        if len(str(account_number)) < 8:
            print("Minimum 8 digits required*")
        else:
            name = input("Enter account holder's name: ")
            initial_balance = float(input("Enter initial balance : "))
            bank.create_account(account_number, name, initial_balance)
            break