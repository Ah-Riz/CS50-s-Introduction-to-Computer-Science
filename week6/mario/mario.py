def main():
    height = get_height()
    print_pyramid(height)

def get_height():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                return height
            else:
                print("Please enter a number between 1 and 8.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def print_pyramid(height):
    for i in range(height):
        print(" " * (height - i - 1) + "#" * (i + 1) + "  " + "#" * (i + 1))

if __name__ == "__main__":
    main()