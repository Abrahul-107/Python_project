def transferMoney(bank):
    sender_account = input("Enter sender's account number: ")
    if len(sender_account) >= 8 and sender_account.isdigit():
        receiver_account = input("Enter receiver's account number: ")
        if(not sender_account==receiver_account) :
            if len(receiver_account) >= 8 and receiver_account.isdigit():
                amount = float(input("Enter amount to send: "))
                bank.send_money(sender_account, receiver_account, amount)
            else:
                print("Enter a valid receiver's account number")
        else:
            print("Sender and reciver account can not be same")
    else:
        print("Enter a valid sender's account number")