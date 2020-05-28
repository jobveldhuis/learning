# Create a Mario-pyramid with an amount of user-specified triangles
# Start a loop that only breaks when we tell it to (when certain conditions are met)
while True:
    # Try, because input could also be a string or something else.
    try:
        # User input
        s = int(input("How many triangles? "))

        # Validate input when input is integer
        if s > 0 and s < 9:
            break
        if s > 9:
            print("Invalid input. Please enter a number lower than 8.")
        if s <= 0:
            print("Invalid input. Please enter a positive integer.")

    # Exceptionhandling when ValueError (string when should be int)
    except ValueError:
        print("Invalid input. Please enter a integer.")
        continue

# Print the pyramid
for r in range(s):
    print(" " * (-r + (s - 1)) + "#" * (r + 1) + " " * 2 + "#" * (r + 1))
