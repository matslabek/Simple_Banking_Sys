import random
import sqlite3


class Account:
    def __init__(self, accounts):
        self.number = self.id_generator(accounts)
        self.pin = Account.pin_generator()
        self.balance = 0

    def id_generator(self, accounts):
        """Method generating a unique account number"""
        iin = '400000'  # Issuer Identification Number
        account_identifier = random.randint(0, 999999999)
        str_ac_id = str(account_identifier)
        # a loop for adding initial zeros
        while len(str_ac_id) < 9:
            str_ac_id = '0' + str_ac_id
        # A loop checking if the generated id is unique
        while int(str_ac_id) in accounts:
            account_identifier = random.randint(0, 999999999)
            str_ac_id = str(account_identifier)
            while len(str_ac_id) < 9:
                str_ac_id = '0' + str_ac_id
        checksum = str(self.luhn(iin + str_ac_id))
        return int(iin + str_ac_id + checksum)

    @staticmethod
    def pin_generator():
        """Generates a pin for the card"""
        return ''.join(map(str, random.sample(range(0, 9), 4)))

    @staticmethod
    def luhn(acc_no):
        """Method implementing Luhn alogorithm, returns the integer, one-digit checksum"""
        digits = [int(di) for di in acc_no]
        odd = True
        i = 0
        for di in digits:
            if odd:
                di = di * 2
                if di >= 10:
                    di -= 9
                digits[i] = di
            if not odd:
                odd = True
            else:
                odd = False
            i += 1
        rest = sum(digits) % 10
        return 10 - rest if rest else rest


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("card.s3db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS card"
            "(id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")

    def __del__(self):
        self.conn.close()

    def add(self, account):
        """Adds a new account to the database"""
        self.cursor.execute('INSERT INTO card (number, pin) VALUES (?, ?);', (account.number, account.pin))
        self.conn.commit()
        print("Your card has been created!\n"
              "\nYour card number:")
        print(account.number)
        print("Your card PIN:")
        print(account.pin)

    def set_balance(self, number, balance):
        """Sets the balance of an account"""
        self.cursor.execute(f'UPDATE card SET balance = {balance} WHERE number={number};')
        self.conn.commit()

    def get_acc(self, number):
        """If the account with the given number exists in the database, it's returned"""
        acc = self.cursor.execute(f'SELECT * FROM card WHERE number={number};').fetchone()
        if acc:
            all_accs = self.all_acc_numbs()
            account = Account(all_accs)
            account.number = int(acc[1])
            account.pin = int(acc[2])
            account.balance = acc[3]
            return account
        return None

    def close_acc(self, number):
        """Deletes the account from database"""
        self.cursor.execute(f'DELETE FROM card WHERE number={number};')
        self.conn.commit()

    def all_acc_numbs(self):
        """Instrumental method returning a list of all account numbers (for lookup)"""
        all_accs = self.cursor.execute('SELECT number from card;').fetchall()
        return [a[0] for a in all_accs]


class Program:
    def __init__(self):
        self.db = Database()
        self.start()
        self.current_account = None

    def start(self):
        """Method that provides a menu for the user to interact with, using an infinite loop"""
        while True:
            option = input("1. Create an account\n"
                           "2. Log into account\n"
                           "0. Exit\n"
                           ":")
            if option == '1':
                accounts = self.db.all_acc_numbs()
                new_acc = Account(accounts)
                self.db.add(new_acc)
            elif option == '2':
                self.log_in()
            elif option == '0':
                print('Bye!')
                break
            else:
                print('Please choose a valid option')

    def account_managing(self, acc):
        """Provides interface for the account management"""
        while True:
            man_opt = input("1. Balance\n"
                            "2. Add income\n"
                            "3. Do transfer\n"
                            "4. Close account\n"
                            "5. Log out\n"
                            "0. Exit\n"
                            ":")
            if man_opt == '1':
                print('Your balance:', acc.balance)
            elif man_opt == '2':
                self.add_income()
            elif man_opt == '3':
                self.transfer()
            elif man_opt == '4':
                self.delete_account()
                break
            elif man_opt == '5':
                print("You have successfully logged out!")
                break
            else:
                print('Bye!')
                exit()

    def add_income(self):
        """Adds income to the current account"""
        income = int(input('Enter the deposit amount'))
        self.current_account.balance += income
        self.db.set_balance(self.current_account.number, self.current_account.balance)
        print('Income was added!\n')

    def transfer(self):
        """Transfers money to another account"""
        receiver = input("\nTransfer\nEnter card number:")
        if int(receiver) == self.current_account.number:
            print("You can't transfer money to the same account!")
        else:
            if Account.luhn(receiver[:-1]) != int(receiver[-1]):    #Luhn algorithm check
                print("Probably you made a mistake in the card number. Please try again!")
            elif receiver not in self.db.all_acc_numbs():
                print("Such a card does not exist.")
            else:
                transfer_am = int(input('Enter how much money you want to transfer:'))
                if transfer_am > self.current_account.balance:
                    print('Not enough money!')
                else:
                    self.current_account.balance -= transfer_am
                    self.db.set_balance(self.current_account.number, self.current_account.balance)
                    receiver_acc = self.db.get_acc(receiver)
                    receiver_acc.balance += transfer_am
                    self.db.set_balance(str(receiver_acc.number), receiver_acc.balance)
                    print('Success!')

    def delete_account(self):
        self.db.close_acc(self.current_account.number)
        print('\nThe account has been closed!\n')

    def log_in(self):
        try:
            card_numb = int(input("Enter your card number:\n"))
            pin_numb = int(input("Enter your PIN:\n"))
            account = self.db.get_acc(card_numb)
            if account:
                if int(account.pin) == pin_numb:
                    print('You have successfully logged in!\n')
                    self.current_account = account
                    self.account_managing(self.current_account)
                else:
                    print('Wrong account number or PIN!\n')
            else:
                print('Wrong account number or PIN!\n')
        except ValueError:
            print("You didn't enter a number...")


my_bank = Program()
