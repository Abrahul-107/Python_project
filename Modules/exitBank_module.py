def exitBank(bank):
    print("Exiting the Bank Management System. Goodbye!")
    print("Account Details:")
    for account_number, account_info in bank._accounts.items():
        print(f"Account Number: {account_number}")
        print(f"Name: {account_info['name']}")
        print(f"Balance: {account_info['balance']}")
        break