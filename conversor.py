'''
USAGE:
With python installed, open a terminal and write
'python conversor.py VALUE'
VALUE being a decimal, hexadecimal(0x), octal(0o) or binary(0b) number
'''
from enum import Enum
import sys
import os

class Numtype(Enum):
    DEC = 0
    HEX = 1
    OCT = 2
    BIN = 3

if len(sys.argv) != 2 or "help" in sys.argv[1]:
    print("Usage: " + os.path.basename(__file__) + " VALUE\n")
    print("VALUE: decimal, hexadecimal(0x), octal(0o) or binary(0b) number")
else:
    arg = str(sys.argv[1])
    res = ""
    number_type = Numtype.DEC
    if "0x" in arg:
        number_type = Numtype.HEX
    elif "0o" in arg:
        number_type = Numtype.OCT
    elif "0b" in arg:
        number_type = Numtype.BIN

    if number_type != Numtype.DEC:
        dec = int(arg, 0)
    else:
        dec = int(arg)

    res += str(dec) + "\n"

    if number_type != Numtype.HEX:
        hexd = hex(dec)
    else:
        hexd = arg

    res += str(hexd) + "\n"

    if number_type != Numtype.OCT:
        octn = oct(dec)
    else:
        octn = arg

    res += str(octn) + "\n"

    if number_type != Numtype.BIN:
        binn = bin(dec)
    else:
        binn = arg

    res += str(binn) + "\n"

    print(res)