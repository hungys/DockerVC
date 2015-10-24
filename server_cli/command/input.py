def input_list(args):
    print args

def input_create(args):
    print args

def input_update(args):
    print args

def input_delete(args):
    print args

def execute(args):
    if args[1] == "list":
        input_list(args)
    elif args[1] == "create":
        input_create(args)
    elif args[1] == "update":
        input_update(args)
    elif args[1] == "delete":
        input_delete(args)