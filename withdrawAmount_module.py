def withdrawAmount(bank):
    account_number = input("Enter account number: ")
    amount = float(input("Enter withdrawal amount: "))
    bank.withdraw(account_number, amount)