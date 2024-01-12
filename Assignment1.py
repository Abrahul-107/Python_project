from bank_module import Bank
from Modules.createAccount_module import createAccount
from Python_project.Modules.depositAmount_module import depositAmount
from Modules.withdrawAmount_module import withdrawAmount
from Modules.checkBalance_module import checkBalance
from Modules.transferMoney_module import transferMoney
from Modules.exitBank_module import exitBank




def main():
    
    # Creating a Bank object
    bank = Bank()

    #And this is will work according to the below statements 
    while True:
        print("\nBank Management System Menu:")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Send Money")
        print("6. Exit")

        choice = int(input("Enter your choice (1-6): "))

        if choice == 1:
            createAccount(bank)  
        elif choice == 2:
            depositAmount(bank)
        elif choice == 3:
            withdrawAmount(bank)
        elif choice == 4:
            checkBalance(bank)
        elif choice == 5:
            transferMoney(bank)
        elif choice == 6:
            exitBank(bank)
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")





if __name__ == "__main__":
    main()
