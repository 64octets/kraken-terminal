#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# This program uses python2-krakenex api package

import krakenex
import os
import helpers as h

optionMap = {
    'a': 'getAccountBalance',
    'b': 'openChart',
    't': 'getTradeBalance',
    'p': 'getTicker',
    'o': 'getOrders',
    'q': 'exit'
}

def dispatch(self, option):

    # Check if
    try:

        # Option
        if option not in optionMap:
            print("\nInvalid option!\n")
            return True

        if option == "q":
            print("\nGoodbye!")
            return False

        method_name = optionMap[str(option)]
        method = getattr(self, method_name)

    except AttributeError:
        print("Unexpected Error: Incorrect optionMap")
        return False
    else:
        print("\n" + method()['txt'] + "\n")
        return True

# Start
os.system('clear')

print("""
    Welcome to your Kraken Utility!
    Choose one of the following options:

    a) Get Account Balance
    t) Get Trade Balance
    p) Get Price EUR/XBT
    o) Get Orders
    b) Open Chart in Browser
    q) Exit
""")

running = True

while running:

    # User prompt for option
    running = dispatch(h, input(">"))

# Give me a bit of space at the end!
print("")
