# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import createDump
import registry


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    reg = registry.registry("registryTest.txt")
    reg.createDumpFromRegistry("out.txt")
    #print(createDump.CSVToDump("C:/Users/f8col/Desktop/Database/FinalProject/baseballdatabank-2023.1/core/ManagersHalf.csv"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
