from django.shortcuts import render

def diagnoz_mkb(code: str) -> str:
    code = code.strip().upper()
    first = code[0]
    if first in "AB":
        return "A"
    elif first == "C" or (first == "D" and code[1] in "01234"):
        return "C"
    elif first == "D" and code[1] in "56789":
        return "D"
    elif first in "EFGHIJKLMNOPQRZU":
        return first
    elif first == "H":
        return "H0" if code[1] in "012345" else "H6"
    elif first in "ST":
        return "T"
    elif first == "VWXY":
        return "V"    


