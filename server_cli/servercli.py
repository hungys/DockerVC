import sys
import command.user as mod_user
import command.project as mod_project
import command.app as mod_app
import command.input as mod_input

base_url = "http://localhost:5000"

def execute_command(command):
    token = command.split(" ")
    if token[0] == "user":
        mod_user.execute(base_url, token)
    elif token[0] == "project":
        mod_project.execute(base_url, token)
    elif token[0] == "app":
        mod_app.execute(base_url, token)
    elif token[0] == "input":
        mod_input.execute(base_url, token)
    elif token[0] == "exit":
        sys.exit(0)

def main_loop():
    while True:
        command = raw_input("> ")
        execute_command(command)

if __name__ == '__main__':
    main_loop()