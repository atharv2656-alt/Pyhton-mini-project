
#   RANDOM PASSWORD GENERATOR  -  Python Mini Project
import random
import string
import math
from datetime import datetime

rng = random.SystemRandom()           
FILE_NAME = "passwords.txt"
WEAK_PASSWORDS = ["123456", "12345678", "abc123", "admin", "letmein",
                  "password", "qwerty", "welcome"]


heading = lambda text: print(f"\n===== {text} =====")



def get_number(message, low, high):
    """Ask until the user enters a valid number (exception handling)."""
    while True:
        try:
            number = int(input(message))
            if low <= number <= high:
                return number
            print(f"Enter a number between {low} and {high}.")
        except ValueError:
            print("Invalid input! Enter a whole number.")


def ask_yes_no(message):
    while True:
        answer = input(message + " (y/n): ").lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("Please type y or n.")


def generate_password(length=12, upper=True, digits=True, symbols=True):
    """Default arguments: all options are ON unless changed."""
    pools = [string.ascii_lowercase]
    if upper:
        pools.append(string.ascii_uppercase)
    if digits:
        pools.append(string.digits)
    if symbols:
        pools.append(string.punctuation)

    password = [rng.choice(pool) for pool in pools]

    all_chars = "".join(pools)
    while len(password) < length:
        password.append(rng.choice(all_chars))

    rng.shuffle(password)
    return "".join(password), len(all_chars)


def generate_pin(length):
    return "".join([str(rng.randint(0, 9)) for i in range(length)])


def generate_passphrase(words):
    word_list = ["tiger", "river", "cloud", "pixel", "maple", "rocket",
                 "ocean", "falcon", "lunar", "ember", "coral", "storm"]
    chosen = rng.sample(word_list, words)
    chosen = [w.capitalize() for w in chosen]
    return "-".join(chosen) + "-" + str(rng.randint(10, 99))


def calculate_strength(length, pool_size):
    """Entropy = length x log2(pool size)"""
    entropy = length * math.log2(pool_size)
    if entropy < 40:
        label = "Weak"
    elif entropy < 60:
        label = "Moderate"
    elif entropy < 80:
        label = "Strong"
    else:
        label = "Very Strong"
    return round(entropy, 1), label


def binary_search(items, target):
    """Items must be sorted. Returns index or -1."""
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def linear_search(text, character):
    """Returns the first index of the character or -1."""
    for i in range(len(text)):
        if text[i] == character:
            return i
    return -1



def save_password(label, password):
    time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open(FILE_NAME, "a") as f:
        f.write(f"{time_now} | {label} | {password}\n")
    print("Saved to", FILE_NAME)


def view_saved():
    try:
        with open(FILE_NAME, "r") as f:
            lines = f.readlines()
        if len(lines) == 0:
            print("No saved passwords.")
        for number, line in enumerate(lines, 1):
            print(f"{number}. {line.strip()}")
    except FileNotFoundError:
        print("No saved passwords yet.")



def option_password():
    heading("GENERATE PASSWORD")
    length = get_number("Password length (4-64): ", 4, 64)
    upper = ask_yes_no("Include uppercase letters?")
    digits = ask_yes_no("Include digits?")
    symbols = ask_yes_no("Include symbols?")
    count = get_number("How many passwords (1-10): ", 1, 10)

    for i in range(count):
        password, pool_size = generate_password(length, upper, digits, symbols)
        print(f"{i + 1}. {password}")

    entropy, label = calculate_strength(length, pool_size)
    print(f"Entropy: {entropy} bits  |  Strength: {label}")
    if ask_yes_no("Save the last password?"):
        save_password("Password", password)


def option_pin():
    heading("GENERATE PIN")
    pin = generate_pin(get_number("PIN length (4-12): ", 4, 12))
    print("Your PIN:", pin)
    if ask_yes_no("Save it?"):
        save_password("PIN", pin)


def option_passphrase():
    heading("GENERATE PASSPHRASE")
    phrase = generate_passphrase(get_number("Number of words (2-8): ", 2, 8))
    print("Your passphrase:", phrase)
    if ask_yes_no("Save it?"):
        save_password("Passphrase", phrase)


def option_check():
    heading("CHECK YOUR PASSWORD")
    password = input("Enter a password: ")
    if password == "":
        print("Password cannot be empty!")
        return

    
    pool_size = 0
    if set(password) & set(string.ascii_lowercase):
        pool_size += 26
    if set(password) & set(string.ascii_uppercase):
        pool_size += 26
    if set(password) & set(string.digits):
        pool_size += 10
    if set(password) & set(string.punctuation):
        pool_size += len(string.punctuation)
    if pool_size == 0:
        print("No letters, digits or symbols found.")
        return

    entropy, label = calculate_strength(len(password), pool_size)
    print(f"Length: {len(password)}")
    print(f"Unique characters: {len(set(password))}")
    print(f"Possible combinations: {math.pow(pool_size, len(password)):.2e}")
    print(f"Entropy: {entropy} bits  |  Strength: {label}")

    if binary_search(sorted(WEAK_PASSWORDS), password.lower()) != -1:
        print("WARNING: This is a very common password!")

    ch = input("Search a character in the password (Enter to skip): ")
    if ch != "":
        position = linear_search(password, ch[0])
        if position == -1:
            print("Character not found.")
        else:
            print("Found at index", position)



def main():
    print("=" * 40)
    print("     RANDOM PASSWORD GENERATOR")
    print("=" * 40)

    menu = {"1": option_password, "2": option_pin, "3": option_passphrase,
            "4": option_check, "5": view_saved}

    while True:
        print("\n1. Generate Password")
        print("2. Generate PIN")
        print("3. Generate Passphrase")
        print("4. Check Password Strength")
        print("5. View Saved Passwords")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "0":
            print("Goodbye!")
            break
        elif choice in menu:
            menu[choice]()
        else:
            print("Invalid choice, try again.")


main()
