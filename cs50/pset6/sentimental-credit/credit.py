import sys


def main():
    # Get user credit card input
    cc = str(get_input())

    # Check if length is invalid
    check_length(cc)

    # Create an array out of inverted cc string
    arr = list(cc[::-1])

    # Let's do the magic and validate the number
    if validate(arr):
        print(get_company(len(cc), cc[0]))
    else:
        is_invalid()

    sys.exit()


def validate(list):
    even = 0
    odd = 0

    for i in range(len(list)):
        n = int(list[i])
        if (i+1) % 2 == 0:
            m = 2 * n
            if m > 9:
                even += m // 10
                even += m % 10
            else:
                even += m
        else:
            odd += n

    sum = even + odd
    if sum % 10 == 0:
        return True

    return False


# Will prompt the user to input credit card number
def get_input():
    while True:
        try:
            # User input
            n = int(input("CC: "))

        # Exceptionhandling when ValueError (string when should be int)
        except ValueError:
            print("Invalid input. Please enter only numbers.")
            continue
        break

    return n


# Will check the length of the creditcard number
def check_length(cc):
    if len(cc) == 13 or len(cc) == 15 or len(cc) == 16:
        return
    else:
        is_invalid()


# Will get the credit card company
def get_company(l, f):
    # Force the input to integers
    l = int(l)
    f = int(f)

    if l == 13:
        return "VISA\n"

    if l == 15:
        return "AMEX\n"

    if f == 4:
        return "VISA\n"

    return "MASTERCARD\n"


# Will print that number was invalid and exit the program
def is_invalid():
    print("INVALID\n")
    sys.exit()


# Calls the program
if __name__ == "__main__":
    main()