#!/usr/bin/env python
# coding: utf-8

import sys
import os

def about():
    print("Running in debug")

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1] 
        if command == "main":
            pass
        else:
            pass
    else:
        about()
    print("All done, closing..")

# wow very main
if __name__ == "__main__":
    sys.exit(main())
