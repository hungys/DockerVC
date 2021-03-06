import sys
import command.user as mod_user
import command.project as mod_project
import command.app as mod_app

def execute_command(command):
    token = command.split(" ")
    if token[0] == "user":
        mod_user.execute(token)
    elif token[0] == "project":
        mod_project.execute(token)
    elif token[0] == "app":
        mod_app.execute(token)
    elif token[0] == "help":
        mod_user.display_help()
        mod_project.display_help()
        mod_app.display_help()
    elif token[0] == "exit":
        sys.exit(0)

def main_loop():
    while True:
        command = raw_input("> ")
        execute_command(command)

if __name__ == '__main__':
    main_loop()