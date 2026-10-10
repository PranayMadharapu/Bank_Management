import json
import random
import string
from pathlib import Path


class Bank:
    database = "data.json"
    data = []

    @classmethod
    def load_data(cls):
        try:
            if Path(cls.database).exists():
                with open(cls.database, "r", encoding="utf-8") as fs:
                    cls.data = json.load(fs)
            else:
                cls.data = []

        except (json.JSONDecodeError, OSError):
            cls.data = []

    @classmethod
    def __update(cls):
        with open(cls.database, "w", encoding="utf-8") as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def __accountgenerate(cls):

        while True:

            alph = random.choices(string.ascii_letters, k=3)
            num = random.choices(string.digits, k=3)
            spchar = random.choices("!@#$%^&*", k=1)

            account_id = alph + num + spchar

            random.shuffle(account_id)

            account_no = "".join(account_id)

            # Make sure account number is unique
            if not any(
                user["accountNo."] == account_no
                for user in cls.data
            ):
                return account_no

    @classmethod
    def find_user(cls, account_no, pin):

        for user in cls.data:

            if (
                user["accountNo."] == account_no
                and user["pin"] == pin
            ):
                return user

        return None

    @classmethod
    def create_account(cls, name, age, email, pin):

        if not name.strip():
            return False, "Name cannot be empty.", None

        if age < 18:
            return False, "You must be at least 18 years old.", None

        if not email.strip():
            return False, "Email cannot be empty.", None

        if len(str(pin)) != 4:
            return False, "PIN must be exactly 4 digits.", None

        info = {
            "name": name.strip(),
            "age": age,
            "email": email.strip(),
            "pin": pin,
            "accountNo.": cls.__accountgenerate(),
            "balance": 0
        }

        cls.data.append(info)

        cls.__update()

        return True, "Account created successfully.", info

    @classmethod
    def deposit(cls, account_no, pin, amount):

        user = cls.find_user(account_no, pin)

        if not user:
            return False, "Account not found or PIN is incorrect.", None

        if amount <= 0:
            return False, "Amount must be greater than zero.", None

        user["balance"] += amount

        cls.__update()

        return True, "Money deposited successfully.", user["balance"]

    @classmethod
    def withdraw(cls, account_no, pin, amount):

        user = cls.find_user(account_no, pin)

        if not user:
            return False, "Account not found or PIN is incorrect.", None

        if amount <= 0:
            return False, "Amount must be greater than zero.", None

        if user["balance"] < amount:
            return False, "Insufficient balance.", None

        user["balance"] -= amount

        cls.__update()

        return True, "Money withdrawn successfully.", user["balance"]

    @classmethod
    def update_account(
        cls,
        account_no,
        pin,
        name=None,
        email=None,
        new_pin=None
    ):

        user = cls.find_user(account_no, pin)

        if not user:
            return False, "Account not found or PIN is incorrect.", None

        if name and name.strip():
            user["name"] = name.strip()

        if email and email.strip():
            user["email"] = email.strip()

        if new_pin is not None:

            if len(str(new_pin)) != 4:
                return False, "New PIN must be exactly 4 digits.", None

            user["pin"] = new_pin

        cls.__update()

        return True, "Account details updated successfully.", user

    @classmethod
    def delete_account(cls, account_no, pin):

        user = cls.find_user(account_no, pin)

        if not user:
            return False, "Account not found or PIN is incorrect."

        cls.data.remove(user)

        cls.__update()

        return True, "Account deleted successfully."


# Load existing accounts when the program starts
Bank.load_data()