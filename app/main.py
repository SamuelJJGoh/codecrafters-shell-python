import sys


def main():


    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()

        if command == "exit":
            break
        elif "echo" in command:
            output = command.replace("echo", "").strip()
            print(output)
            main()
            break
        
        print(f"{command}: command not found")

        



if __name__ == "__main__":
    main()
