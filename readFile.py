import csv


def load_menu(filename):
    menu = {}
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            menu[row[0]] = int(row[1])

    return menu
