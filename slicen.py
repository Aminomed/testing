#!/usr/bin/python3
import sys

#main Funktion
def main(args):
    n = int(args[0])
    lis = list(range(n+1))

    #erste 10 Zahlen
    print(lis[:10])

    #letzte 10 Zahlen
    print(lis[-10:])

    #jede 10te Zahl
    print(lis[::10])

    #jede dritte Zahl aber davon nicht die ersten vier und nicht die letzten fünf
    print(lis[4::3][:-5])

    if len(args) == 2:
        name = args[1]
        name = name[0] +"X" + name[2:]
        print(name)


if __name__ == "__main__":
    main(sys.argv[1:])