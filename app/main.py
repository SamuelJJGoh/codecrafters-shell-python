import sys
import os
import subprocess
import shlex

def main():

    built_in_commands = ["echo", "exit", "type", "pwd", "cd"]

    while True:
        sys.stdout.write("$ ")
        command = input()
                
        if command.startswith("type"): 
            check_command = command.replace("type", "", 1).strip()
            if check_command == "":
                continue
            elif check_command in built_in_commands :
                print(f"{check_command} is a shell builtin")
            else :
                all_paths = os.environ["PATH"]
                directories = all_paths.split(":")
                found_path = None
                for directory in directories :
                    potential_executable = directory + "/" + check_command
                    if os.path.isfile(potential_executable) and os.access(potential_executable, os.X_OK) :
                        found_path = potential_executable
                        break
                if found_path:
                    print(f"{check_command} is {found_path}")
                else:
                    print(f"{check_command}: not found")
            continue

        elif command.strip() == "exit":
            break  

        elif command.startswith("echo"):
            parts = shlex.split(command)
            args = parts[1:] if len(parts) > 1 else []
            print(" ".join(args))
            continue
        
        elif command == "pwd":
            print(os.getcwd())
            continue

        elif command.startswith("cd"):
            target_directory = command.replace("cd", "", 1).strip()
            if target_directory == "~":
                home_directory = os.environ["HOME"]
                os.chdir(home_directory)
            elif os.path.isdir(target_directory):
                os.chdir(target_directory)
            else :
                print(f"cd: {target_directory}: No such file or directory")   
            continue
        
        else : 
            parts = shlex.split(command)
            program_name, *args = parts
            all_paths = os.environ["PATH"]
            directories = all_paths.split(":")
            found_executable = False
            for directory in directories :
                potential_executable = directory + "/" + program_name
                if os.path.isfile(potential_executable) and os.access(potential_executable, os.X_OK) :
                    subprocess.call([program_name, *args])
                    found_executable = True
                    break
                else : 
                    continue
            if found_executable :
                continue
        print(f"{command}: command not found")

if __name__ == "__main__":
    main()
