import re

def main():
    number = get_number()
    check_credit_card(number)

def check_credit_card(number):
    creditcard_list = {
        "VISA": r"^4\d{12}(?:\d{3})?$",
        "MASTERCARD": r"^5[1-5]\d{14}$",
        "AMEX": r"^3[47]\d{13}$",
    }
    for card_type, pattern in creditcard_list.items():
        if re.match(pattern, str(number)):
            print(card_type)
    else:
        print("INVALID")

def get_number():
    try:
        number = int(input("Number: "))
    except ValueError:
        print("That's not a valid number. Please try again.")
        return get_number()
    else:
        return number

if __name__ == "__main__":
    main()