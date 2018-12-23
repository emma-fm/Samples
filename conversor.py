'''
USAGE:
With python installed, open a terminal and write
'python conversor.py VALUE'
VALUE being a decimal, hexadecimal(0x), octal(0o) or binary(0b) number
'''
import sys
import os

if len(sys.argv) != 2 or "help" in sys.argv[1]:
    print("Usage: " + os.path.basename(__file__) + " VALUE\n")
    print("VALUE: decimal, hexadecimal(0x), octal(0o) or binary(0b) number")
else:
    arg = str(sys.argv[1])
    dec = int(arg, 0)
    print(str(dec) + "\n" + str(hex(dec)) + "\n" + str(oct(dec)) + "\n" + str(bin(dec)))