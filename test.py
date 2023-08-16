list = [1, 2, 3, 4, 5]


def list_loop(action):
    for item in list:
        item_as_string = str(item)
        action(item_as_string)


def print_item_as_string(item):
    print(item)
