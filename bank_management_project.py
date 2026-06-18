''' context 

1)Bank account for users
2)Deposite money
3)Withdraw money
4)Details
5)Update details
6)Delete account
7)Check balance
8)Exit

'''
import json
import string
import random
from pathlib import Path

class Bank:
    database = "data.json"
    data = []
    
    try:
        if Path(database).exists(): 
            with open(database) as fs:
                data = json.loads(fs.read())
        else: 
            print("file not found")
    except Exception as err:
        print(f"Error occured as {err}")
        
    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            json.dump(cls.data, fs, indent=4)
            
    @classmethod
    def __generateAccountNumber(cls):
        alpha = random.choices(string.ascii_letters, k = 3)
        spChar = random.choices("!@#$%^&*", k = 1)
        num = random.choices(string.digits, k = 5)
        generatedPin = alpha + spChar + num
        random.shuffle(generatedPin)
        return "".join(generatedPin) 
    
    @classmethod
    def findUser(cls, accNo, pin):
        for user in cls.data:
            if user["account number"] == accNo and user["pin"] == pin:
                return user
        return None   
    
    def authenticate(self):
        accNo = input("Enter account number : ")

        try:
            accPin = int(input("Enter pin : "))
        except ValueError:
            print("Pin must be numeric")
            return None

        return Bank.findUser(accNo, accPin)
            
        
    def createAccount(self): 

        info = {
            "name": input("Enter name : "),
            "age": int(input("Enter age : ")),
            "email": input("Enter e-mail : "),
            "pin": int(input("Enter pin(4 digits) : ")),
            "account number": Bank.__generateAccountNumber(),
            "balance": 0
            }               
        
        if '@' not in info['email'] or '.' not in info['email']:
            print("Invalid email")
            return

        if any(user['email'] == info['email'] for user in Bank.data):
            print("Email already registered")
            return
        
        if info["age"] < 18 :
            print("Sorry..! you are not eligible to create your account")  
        
        elif len(str(info['pin'])) != 4:
            print("Your pin must be 4 digits")
            
        else:
            print("\nAccount has been created successfully")
            for i in info:
                print(f"{i} : {info[i]}")
            print("\nPlease note down your account number")
                
            Bank.data.append(info)
            Bank.__update()
            
    def depositMoney(self):
        userData = self.authenticate()

        if not userData:
            print("Account not found")
            return

        try:
            amount = int(input("Enter deposit amount : "))
        except ValueError:
            print("Amount must be numeric")
            return
        
        if amount <= 0:
            print("Amount must be greater than 0")
        else:
            userData["balance"] += amount
            Bank.__update()
            print("Amount deposited successfully")
                
    def withdrawMoney(self):
        userData = self.authenticate()

        if not userData:
            print("Account not found")
            return

        try:
            amount = int(input("Enter withdraw amount : "))
        except ValueError:
            print("Amount must be numeric")
            return

        if amount <= 0:
            print("Invalid amount")
        elif userData['balance'] < amount:
            print(f"Amount is not sufficient to withdraw {amount}")
        else:
            userData["balance"] -= amount
            Bank.__update()
            print("Amount withdrew successfully")
                
    def showDetails(self):
        userData = self.authenticate()

        if not userData:
            print("Account not found")
            return
        
        print("Your information are : ")
        for key, value in userData.items():
            if key == "pin":
                print("pin : ****")
            else:
                print(f"{key} : {value}")
            
    def updateDetails(self):
        userData = self.authenticate()

        if not userData:
            print("Account not found")
            return
        
        print("Fill the details to change otherwise leave it")
        newData = {
            "name":input("Enter new name : "),
            "email":input("Enter new email : "),
            "pin":input("Enter new pin : ")
        }
        
        if newData["name"] == "":
            newData["name"] = userData["name"]
            
        if newData["email"] == "":
            newData["email"] = userData["email"]
            
        if newData["pin"] == "":
            newData["pin"] = userData["pin"]
            
        newData["age"] = userData["age"]
        newData["account number"] = userData["account number"]
        newData["balance"] = userData["balance"]
        
        if (
            newData["email"] != userData["email"]
            and ('@' not in newData["email"] or '.' not in newData["email"])
        ):
            print("Invalid email")
            return
        
        if any(
            user["email"] == newData["email"]
            and user["account number"] != userData["account number"]
            for user in Bank.data
        ):
            print("Email already registered")
            return
        
        if isinstance(newData["pin"], str):
            if not newData["pin"].isdigit() or len(newData["pin"]) != 4:
                print("Pin must be exactly 4 digits")
                return

            newData["pin"] = int(newData["pin"])
                        
        for i in newData:   
            if newData[i] != userData[i]:
                userData[i] = newData[i]
        
        Bank.__update()
        print("Information updated successfully")
            
    def deleteAcc(self):
        userData = self.authenticate()

        if not userData:
            print("Account not found")
            return
        
        check = input("Press y to delete or n:")
        if check.lower() == 'y':
            index = Bank.data.index(userData)
            Bank.data.pop(index)
            Bank.__update()
            print("Account deleted successfully")
        else:
            print("Your account is safe")
            
    def checkBalance(self):
        userData = self.authenticate()

        if not userData:
            print("Account not found")
            return

        print(f"Current Balance: ₹{userData['balance']}")
        
                
    
user = Bank()
choice = 0
while choice != 7:
    print("Press 1 for creating an account")
    print("Press 2 for deposite the money")
    print("Press 3 for withdraw the money")
    print("Press 4 for check details")
    print("Press 5 for update details")
    print("Press 6 for detele account")
    print("Press 7 for balance check")
    print("Press 8 for Exit")

    try:
        choice = int(input("Enter your choice : "))
    except ValueError:
        print("Please enter a valid number")
        continue

    if choice == 1:
        user.createAccount()
        
    elif choice == 2:
        user.depositMoney()
        
    elif choice == 3:
        user.withdrawMoney()
        
    elif choice == 4:
        user.showDetails()
        
    elif choice == 5:
        user.updateDetails()
        
    elif choice == 6:
        user.deleteAcc()
        
    elif choice == 7:
        user.checkBalance()
        
    elif choice == 8:
        break
    
    else:
        print("Enter valid choice")
        