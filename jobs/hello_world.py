import os


def main():
    # Create the output directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Write "Hello World" to the file
    with open("data/hello_world.txt", "w") as f:
        f.write("Hello World")

    # List out all packages in the current environment and save to a file
    os.system("pip freeze > data/requirements.txt")


if __name__ == "__main__":
    main()
