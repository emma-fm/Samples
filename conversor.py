from enum import Enum
import sys

class Numtype(Enum):
    DEC = 0
    HEX = 1
    OCT = 2
    BIN = 3

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