import json
import random
import string
from pathlib import Path

class Bank:
    database = 'data.json'
    data =[]

    try:
        if Path(database).exists():
           with open(database, 'r') as fs:
            data = json.loads(fs.read())
        else:
            print("no such file exists")
    except:
        print("error in reading file")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenerate(cls):
        alph = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar =random.choices("!@#$%^&*", k=1)
        id = alph + num + spchar
        random.shuffle(id)
        return ''.join(id)

    def Createaccount(self):
        info = {
            "name " : input("Enter your name: "),
            "age " : int(input("Enter your age: ")),
            "email" : input("Enter your email: "),
            "pin" : int(input("Enter your pin: ")),
            "accountNo." : Bank.__accountgenerate(),
            "balance" : 0
        }
        if(info["age "] < 18):
            print("You are not eligible to create an account")
        else:
            print("Your account has been created successfully")
            for i in info:
                print(i, ":", info[i])
            print("Your account number is: ", info["accountNo."])
            Bank.data.append(info)
            Bank.__update()


    def depositmoney(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]
        if userdata == False:
            print("Account not found or pin is incorrect") 
        else:
            amount = int(input("Enter the amount you want to deposit: "))
            userdata[0]['balance'] += amount
            print("Your new balance is: ", userdata[0]['balance'])
            Bank.__update()


    def withdrawmoney(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("soory no data found")
        else:
            amount = int(input("Enter the amount you want to withdraw: "))
            if userdata[0]['balance'] < amount:
                print("Insufficient balance")
            else:
                userdata[0]['balance'] -= amount
                print("Your new balance is: ", userdata[0]['balance'])
                Bank.__update()

    def showdetails(self):

        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]
        print("your information are \n\n\n")
        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")

    def updatedetails(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("no such user found ")
        
        else:
            print("you cannot change the age, account number, balance")

            print("Fill the details for change or leave it empty if no change")

            newdata = {
                "name": input("please tell new name or press enter : "),
                "email":input("please tell your new Email or press enter to skip :"),
                "pin": input("enter new Pin or press enter to skip: ")
            }

            if newdata["name"] == "":
                newdata["name"] = userdata[0]["name "]
            if newdata["email"] == "":
                newdata["email"] = userdata[0]["email"] 
            if newdata["pin"] == "":
                newdata["pin"] = userdata[0]["pin"] 

            newdata["age "] = userdata[0]["age "]
            newdata["accountNo."] = userdata[0]["accountNo."]   
            newdata["balance"] = userdata[0]["balance"]

            if type(newdata["pin"]) == str:
                newdata["pin"] = int(newdata["pin"])

            for i in newdata:
                userdata[0][i] = newdata[i]
            Bank.__update() 

    def deleteaccount(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("no such user found ")
        
        else:
            check = input("Are you sure you want to delete your account? (yes/no): ")
            if check.lower() != "yes":
                print("Account deletion cancelled.")
                return
            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                Bank.__update()
                print("your account has been deleted successfully")
    

user = Bank()
print("Press 1 for creating a new account")
print("Press 2 for depositing money")
print("Press 3 for withdrawing money")
print("Press 4 for details")
print("Press 5 for updating account details")
print("Press 6 for deleting")

check = int(input("Enter your choice: "))

if(check == 1):
    user.Createaccount()

if(check == 2):
    user.depositmoney()

if(check == 3):
    user.withdrawmoney()

if(check == 4):
    user.showdetails()

if(check == 5):
    user.updatedetails()

if(check ==6):
    user.deleteaccount()
