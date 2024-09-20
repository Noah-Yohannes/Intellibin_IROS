def function1():
    print("This is function 1")

def function2():
    print("This is function 2")

def function3():
    print("This is function 3")

# define a dictionary of functions
switcher = {
    1: function1,
    2: function2,
    3: function3
}

# get the function from the dictionary based on the key
key = 2
switcher.get(key, lambda: print("Invalid key"))()