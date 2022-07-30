import webbrowser


# The commands have been stored a values and keys are the function that will be executed of the commands match

# The get_key() function get teh key for a particular command
def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key


# this function is used to check if the command is available in the dictionary
def check_available(val):
    if val in command_function_dict.values():
        return True
    return False


# this function is used to fire up the function associated with the commands
def fire_up_commands(val):
    comm = get_key(val, command_function_dict)
    comm()


# list of commands that will be used.
def command1():
    print("command1")
    pass


def command2():
    print("command2")
    pass


def command3():
    print("command3")
    pass


def command4():
    print("command4")
    pass


def command5():
    print("command5")
    pass


def command6():
    print("command6")
    pass


def command7():
    print("command7")
    pass


def command8():
    print("command8")
    pass


def command9():
    print("command9")
    pass


def command10():
    print("command10")
    pass


# Dictionary for storing key and values, keys are the function that will be triggered and the values are the commands
# that gets fired off if the value matches

command_function_dict = {command1: [0, 0, 0, 0, 0, 1, 1, 1, 1, 1], command2: [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                         command3: [], command4: [],
                         command5: [], command6: [], command7: [], command8: [], command9: [], command10: []}
