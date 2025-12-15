import sys
import os
import subprocess
import shlex
import readline

built_in_commands = ["echo", "exit", "type", "pwd", "cd"]
all_paths = os.environ["PATH"]
directories = all_paths.split(":")

def completer(text, state):
    matches =  [cmd + " " for cmd in built_in_commands if cmd.startswith(text)]
    
    if state > len(matches):
        return None
    else:
        return matches[state]

def main():

    readline.set_completer(completer)
    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete") # TAB key for macOS
    else:
        readline.parse_and_bind("tab: complete")

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
        
        # echo with redirect/append standard output
        elif command.startswith("echo") and "2>" not in command and "2>>" not in command:
            tokens = shlex.split(command)
            args = tokens[1:] if len(tokens) > 1 else []
            redir_operator = None
            redir_append_operator = None
            if ">" in args:
                redir_operator = ">"
            elif "1>" in args:
                redir_operator ="1>"
            elif ">>" in args:
                redir_append_operator = ">>"
            elif "1>>" in args:
                redir_append_operator = "1>>"
            
            if redir_operator:
                redir_operator_index = args.index(redir_operator)
                redir_args = args[:redir_operator_index]
                redir_file = args[redir_operator_index + 1] 

                with open(redir_file, "w") as f:
                    for arg in redir_args:
                        f.write(f"{arg}\n")
                continue
            elif redir_append_operator:
                redir_append_operator_index = args.index(redir_append_operator)
                redir_append_args = args[:redir_append_operator_index]
                redir_append_file = args[redir_append_operator_index + 1] 

                with open(redir_append_file, "a") as f:
                    for arg in redir_append_args:
                        f.write(f"{arg}\n")
                continue

            print(" ".join(args))
            continue

        # redirect/append standard errors
        elif "2>" in command or "2>>" in command:
            tokens = shlex.split(command)
            program_name = tokens[0]
            args = tokens[1:] if len(tokens) > 1 else []

            redir_operator = None
            redir_append_operator = None

            if "2>" in args:
                redir_operator = "2>"
            elif "2>>" in args:
                redir_append_operator ="2>>"

            if redir_operator:
                redir_operator_index = args.index(redir_operator)
                redir_args = args[:redir_operator_index]
                redir_file = args[redir_operator_index + 1] 

                for directory in directories:
                    potential_executable = directory + "/" + program_name
                    if os.path.isfile(potential_executable) and os.access(potential_executable, os.X_OK):
                        with open(redir_file, "w") as f:
                            subprocess.run([potential_executable, *redir_args], stderr=f)
                        break
                continue
            elif redir_append_operator:
                redir_append_operator_index = args.index(redir_append_operator)
                redir_append_args = args[:redir_append_operator_index]
                redir_append_file = args[redir_append_operator_index + 1] 

                for directory in directories:
                    potential_executable = directory + "/" + program_name
                    if os.path.isfile(potential_executable) and os.access(potential_executable, os.X_OK):
                        with open(redir_append_file, "a") as f:
                            subprocess.run([potential_executable, *redir_append_args], stderr=f)
                        break
                continue
        
        
        # other commands with redirect/append standard output
        elif ">" in command: 
            tokens = shlex.split(command)
            program_name = tokens[0]
            args = tokens[1:] if len(tokens) > 1 else []
            redir_operator = None
            redir_append_operator = None

            if ">" in args:
                redir_operator = ">"
            elif "1>" in args:
                redir_operator ="1>"
            elif ">>" in args:
                redir_append_operator = ">>"
            elif "1>>" in args:
                redir_append_operator = "1>>"
            
            if redir_operator:
                redir_operator_index = args.index(redir_operator)
                redir_args = args[:redir_operator_index]
                redir_file = args[redir_operator_index + 1] 

                for directory in directories:
                    potential_executable = directory + "/" + program_name
                    if os.path.isfile(potential_executable) and os.access(potential_executable, os.X_OK):
                        with open(redir_file, "w") as f:
                            subprocess.run([potential_executable, *redir_args], stdout=f)
                        break
                continue
            elif redir_append_operator:
                redir_append_operator_index = args.index(redir_append_operator)
                redir_append_args = args[:redir_append_operator_index]
                redir_append_file = args[redir_append_operator_index + 1] 

                for directory in directories:
                    potential_executable = directory + "/" + program_name
                    if os.path.isfile(potential_executable) and os.access(potential_executable, os.X_OK):
                        with open(redir_append_file, "a") as f:
                            subprocess.run([potential_executable, *redir_append_args], stdout=f)
                        break
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
            tokens = shlex.split(command)
            program_name, *args = tokens
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
