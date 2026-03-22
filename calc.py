#!/usr/bin/python3
import sys

def compute(v1, op, v2):
    try:
        val1 = float(v1)
        val2 = float(v2)
    except ValueError:
        return None

    if op == '+':
        return val1 + val2
    elif op == '-':
        return val1 - val2
    elif op in ('*', 'x'):
        return val1 * val2
    elif op == '/':
        if val2 == 0.0:
            return None
        return val1 / val2
    else:
        return None

def main(args):
    if len(args) != 3:
        print("Fehler: Bitte genau drei Argumente (Zahl Operator Zahl) übergeben.")
        return

    v1, op, v2 = args
    result = compute(v1, op, v2)

    if result is None:
        print("Fehler: Ungültige Eingaben. Bitte überprüfen Sie die Zahlen und den Operator.")
    else:
        # Optional: Wenn das Ergebnis eine ganze Zahl ist, schneiden wir die Nachkommastellen ab (.0),
        # um wie im Beispiel 3 * 4 = 12 auszugeben.
        if result.is_integer():
            result = int(result)
        
        print(f"{v1} {op} {v2} = {result}")

if __name__ == '__main__':
    # type: ignore is used to bypass a type checker false positive with list slicing
    main(sys.argv[1:])  # type: ignore
