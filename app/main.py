import sys


def main():

    built_in_commands = ["echo", "exit", "type"]

    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()

        if command.startswith("type"):
            check_command = command.replace("type", "", 1).strip()
            print(f"{check_command} is a shell builtin" if check_command in built_in_commands 
                    else  f"{check_command}: not found")
            main()
            break
        elif command == "exit":
            break
        elif "echo" in command:
            output = command.replace("echo", "").strip()
            print(output)
            main()
            break
        
        print(f"{command}: command not found")

        



if __name__ == "__main__":
    main()
