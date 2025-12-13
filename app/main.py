import sys
import os
import subprocess

def main():

    built_in_commands = ["echo", "exit", "type", "pwd"]

    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()

        if command.startswith("type"):
            check_command = command.replace("type", "", 1).strip()
            if check_command == "":
                main()
                break
            elif check_command in built_in_commands :
                print(f"{check_command} is a shell builtin")
            else :
                all_paths = os.environ["PATH"]
                directories = all_paths.split(":")
                for directory in directories :
                    potential_executable = directory + "/" + check_command
                    if os.path.isfile(potential_executable) and os.access(potential_executable, os.X_OK) :
                        print(f"{check_command} is {potential_executable}")
                        main()
                    else :
                        continue
                print(f"{check_command}: not found")
            main()
            break
        elif command == "exit":
            break            
        elif "echo" in command:
            output = command.replace("echo", "").strip()
            print(output)
            main()
            break
        elif command == "pwd":
            print(os.getcwd())
            main()
            break
        else : 
            program_name = command.split(" ")[0]
            args = command.split(" ")[1:]
            all_paths = os.environ["PATH"]
            directories = all_paths.split(":")
            for directory in directories :
                potential_executable = directory + "/" + program_name
                if os.path.isfile(potential_executable) and os.access(potential_executable, os.X_OK) :
                    subprocess.call([program_name, *args])
                    main()
                else : 
                    continue
        print(f"{command}: command not found")

        



if __name__ == "__main__":
    main()
