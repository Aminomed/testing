import sys

de2en = {
    1: "one",
    2: "two",
    3: "three",
    "eins": "one",
    "zwei": "two",
    "drei": "three"
}

def main(args):
    n = args[0]
    print(n + " auf englisch ist ") 
    print(de2en[n])

if __name__ == '__main__':
    main(sys.argv[1:])