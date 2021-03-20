import random as rand
import pyperclip as p
import base64 as b
import os


def askForChoice():
    print("Input is always the number before the option\n")
    choice = input("What do you want:\n1) safe a password from clipboard\n2) get a password\n3) create a "
                   "password\n4) settings\n")
    while True:
        handleChoice(choice)
        choice = input("What do you want: 1) safe a password from clipboard, 2) get a password, 3) create a "
                       "password, 4) settings, 5) break?\n")


def handleChoice(choice):
    if int(choice) == 1:
        while True:
            name = input("What name do you label the password?\n")
            error = checkIfNameExist(name)
            if error == 500:
                print("Already existing password\n")
            else:
                password = p.paste()
                password = password.strip()
                ask = input("Sure to safe this password: " + password + " ? Y/N")
                safePasswordToDatabase([name, password]) if ask == ("Y" or "y" or "Yes" or "yes") else print("Not "
                                                                                                             "saved")
                print(password + " is saved with label '" + name + "'\n")
                break

    elif int(choice) == 2:
        ask = input("Choice: 1) Get all labels, 2) Get password\n")
        if int(ask) == 1:
            getAllLabels()
        elif int(ask) == 2:
            name = input("How did you safe the password? ")
            if name != "wwdoc":
                password = getPassword(name)
                if password != "Password not found":
                    safeToClipboard(password)
                    print("Password is: " + password + " and is copied to clipboard\n")
                else:
                    print("Not found\n")
            else:
                print("No access\n")
        else:
            print("Something wrong\n")

    elif int(choice) == 3:
        """ask = input("1) Only copy to clipboard, or 2) Safe the password and copy to clipboard?\n")
        if int(ask) == 1:
            ask = input("Complicated or not? Y/N")
            if ask == "Y":
                password = generatePassword(1)
            else:
                password = generatePassword(0)
            safeToClipboard(password)
            print("Copied to clipboard: " + password)
        elif int(ask) == 2:"""
        while True:
            name = input("What name do you label the password? ")
            error = checkIfNameExist(name)
            if error == 500:
                print("Already existing password\n")
            else:
                ask = input("Complicated or not? Y/N")
                if ask == "Y":
                    password = generatePassword(1)
                else:
                    password = generatePassword(0)
                safePasswordToDatabase([name, password])
                safeToClipboard(password)
                print(password + " is saved with label '" + name + "'\n")
                break
        """else:
            print("Something wrong\n")"""
    elif int(choice) == 4:
        setting = input("Which setting do you need?\n1) change password\n2) change username\n3) delete passwords\n")
        if int(setting) == 1:
            pass
        elif int(setting) == 2:
            pass
        elif int(setting) == 3:
            pass
        else:
            print("Something wrong")
    else:
        print("Something wrong\n")


def controlName():
    name = input("Wat is your name? ")
    return name


def controlAccess():
    ask = ""
    password = getPassword(user_name + "wwdoc")
    if password == "Password not found":
        ask = input("There is no password found, you need to set one. Give new password: ")
        safePasswordToDatabase([user_name + "wwdoc", ask])
    else:
        while ask != password:
            ask = p.paste()
            if ask == password:
                break
            else:
                ask = input("Password: ")
                if ask != password:
                    print("Wrong password")
                else:
                    break


def generatePassword(add):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    password = ""
    check_uc = False
    check_c = False
    while not check_uc or not check_c:
        password = ""
        x = rand.randint(1, 3)
        for i in range(6):
            if x == 1:
                password += rand.choice(letters)
            else:
                password += rand.choice(letters[0:26])
        password += "-"
        for i in range(6):
            if x == 2:
                password += rand.choice(letters)
            else:
                password += rand.choice(letters[0:26])
        password += "-"
        for i in range(6):
            if x == 3:
                password += rand.choice(letters)
            else:
                password += rand.choice(letters[0:26])
        password += "!" if add == 1 else ""
        check_uc = any(item in letters[26:52] for item in password)
        check_c = any(item in letters[52:] for item in password)
    return password


def safeToClipboard(password):
    p.copy(password)


def decodePassword(password):
    password = b.b64decode(bytes(password, "utf-8"))
    password = str(password, "utf-8")
    return password


def encodePassword(password):
    password = bytes(password, "utf-8")
    password = b.b64encode(password)
    return str(password, "utf-8")


def getPassword(name):
    password = "Password not found"
    file = open("data/passwords.txt", "r")
    for line in file:
        x = line.split("|", 2)
        if (user_name == x[0]) or (user_name == "admin"):
            if name == x[1]:
                password = decodePassword(x[2])
        break
    return password


def checkIfNameExist(name):
    error = 0
    file = open("data/passwords.txt", "r")
    for line in file:
        x = line.split("|")
        if x[1] == name:
            error = 500
            break
    return error


def safePasswordToDatabase(data):
    name = data[0]
    password = data[1]
    password = encodePassword(password)
    file = open("data/passwords.txt", "a")
    file.write(user_name + "|" + name + "|" + password + "\n")


def getAllLabels():
    file = open("data/passwords.txt", "r")
    for line in file:
        x = line.split("|")
        if x[1] != (x[0] + "wwdoc"):
            if user_name == x[0]:
                print(x[1])
            elif user_name == "admin":
                print(x[1])


def tryOpenFile():
    dir_set = os.path.isdir('data')
    if dir_set:
        try:
            file = open("data/passwords.txt", "r")
        except IOError:
            file = open("data/passwords.txt", "x")
    else:
        os.mkdir('data')
        file = open('data/passwords.txt', 'x')
    file.close()


user_name = controlName()
tryOpenFile()
controlAccess()
askForChoice()
