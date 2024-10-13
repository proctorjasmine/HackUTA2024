
exit_code = 100

while True:
    print("Hello welcome to the menu please select an option\n")
    print(" 1. Enter Name\n 2. Enter age\n 3. Enter sex\n 4. exit")

    user_input = input("Please enter your choice: ")

    if user_input == "1":
        name = input("Please enter your name: ")
        print(f"Hello {name}")

    elif user_input == "2":
        age = input("Please enter your age: ")
        print(f"Your age is {age}")

    elif user_input == "3":
        sex = input("Please enter your sex: ")
        print(f"Your sex is {sex}")

    elif user_input == "4":
        exit(exit_code)

    else:
        print("Invalid input")

