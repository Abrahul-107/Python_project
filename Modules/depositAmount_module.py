def depositAmount(bank):
    account_number = input("Enter account number: ")
    amount = float(input("Enter deposit amount: "))
    bank.deposit(account_number, amount)