import random as rand
import pyperclip as p


def askForChoice():
    choice = input("What do you want, 1) safe a password, 2) get a password, 3) create a password?")
    return choice


def safePassword(password):
    password = ""
    return password


def securePassword(password):
    return password


def handleChoice(choice):
    if choice == 1:
        name = input("What name do you label the password?")
    elif choice == 2:
        name = input("How did you safe the password?")
    elif choice == 3:
        ask = input("1) Only copy to clipboard, or 2) Safe the password and copy to clipboard?")
        if ask == 1:
            password = generatePassword()
            safeToClipboard(password)
        elif ask == 2:
            password = generatePassword()
            safeToClipboard(password)
        else:
            print("Something wrong")
    else:
        print("Something wrong")


def generatePassword():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    password = ""
    for i in range(6):
        password += rand.choice(letters[0:26])
    password += "-"
    for i in range(6):
        password += rand.choice(letters[0:26])
    password += "-"
    for i in range(6):
        password += rand.choice(letters)
    return password


def safeToClipboard(password):
    p.copy(password)


def decodePassword(password):
    password.encode()
    return password


def getPassword(name):
    file = open("passwords.txt", "r")
    for line in file:
        line.split("|")
        if name == line[0]:
            password = decodePassword(line[1])
            return password
        break

