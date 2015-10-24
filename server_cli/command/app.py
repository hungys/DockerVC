def app_list(args):
    print args

def app_create(args):
    print args

def app_update(args):
    print args

def app_delete(args):
    print args

def execute(args):
    if args[1] == "list":
        app_list(args)
    elif args[1] == "create":
        app_create(args)
    elif args[1] == "update":
        app_update(args)
    elif args[1] == "delete":
        app_delete(args)