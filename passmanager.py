import random as rand
import pyperclip as p
import base64 as b
import os


def askForChoice():
    print("Input is always the number before the option\n")
    choice = input("What do you want: \n1) safe a password from clipboard \n2) get a password \n3) create a "
                   "password \n")
    while True:
        if int(choice) == 4:
            break
        handleChoice(int(choice))
        choice = input("What do you want: 1) safe a password from clipboard, 2) get a password, 3) create a "
                       "password, 4) break?\n")

def handleChoice(choice):
    if choice == 1:
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

    elif choice == 2:
        ask = input("Choice: 1) Get all labels, 2) Get password\n")
        if int(ask) == 1:
            password = getPassword("wwdoc")
            if password == "Password not found":
                ask = input("There is no password found, you need to set one. Give new password: ")
                safePasswordToDatabase(["wwdoc", ask])
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

    elif choice == 3:
        ask = input("1) Only copy to clipboard, or 2) Safe the password and copy to clipboard?\n")
        if int(ask) == 1:
            ask = input("Complicated or not? Y/N")
            if ask == "Y":
                password = generatePassword(1)
            else:
                password = generatePassword(0)
            safeToClipboard(password)
            print("Copied to clipboard: " + password)
        elif int(ask) == 2:
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
        else:
            print("Something wrong\n")
    else:
        print("Something wrong\n")


def generatePassword(add):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
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
    password += "!" if add == 1 else None
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
        x = line.split("|", 1)
        if name == x[0]:
            password = decodePassword(x[1])
            break
    return password


def checkIfNameExist(name):
    error = 0
    file = open("data/passwords.txt", "r")
    for line in file:
        x = line.split("|")
        if x[0] == name:
            error = 500
            break
    return error


def safePasswordToDatabase(data):
    name = data[0]
    password = data[1]
    password = encodePassword(password)
    file = open("data/passwords.txt", "a")
    file.write(name + "|" + password + "\n")


def getAllLabels():
    file = open("data/passwords.txt", "r")
    for line in file:
        x = line.split("|")
        print(x[0]) if x[0] != "wwdoc" else None


def tryOpenFile():
    dir_isset = os.path.isdir('data')
    if dir_isset:
        try:
            file = open("data/passwords.txt", "r")
        except IOError:
            file = open("data/passwords.txt", "x")
    else:
        os.mkdir('data')
        file = open('data/passwords.txt', 'x')
    file.close()


tryOpenFile()
askForChoice()