import sys

def main():
    if len(sys.argv) < 2:
        print("Bitte geben Sie n als Kommandozeilenargument an.")
        sys.exit(1)
        
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("n muss eine ganze Zahl sein.")
        sys.exit(1)

    # Liste der Zahlen von 0 bis n (inklusive n)
    z = list(range(n + 1))
    
    print(f"--- Slicing Ergebnisse für n = {n} ---")
    
    # die ersten 10 Zahlen
    print("Die ersten 10 Zahlen:", z[:10])
    
    # die letzten 10 Zahlen
    print("Die letzten 10 Zahlen:", z[-10:])
    
    # jede 10.te Zahl (beginnend mit 0)
    print("Jede 10.te Zahl:", z[::10])
    
    # die mittlere Zahl
    # Bei gerader Anzahl Elemente gibt es zwei mittlere, wir nehmen das /2 (Standard in Python)
    print("Die mittlere Zahl:", z[len(z)//2] if z else None)
    
    # jede dritte Zahl außer von den ersten vier und von den letzten fünf
    # D.h. aus der Liste ohne die ersten 4 und letzten 5 Elemente jede 3. Zahl
    print("Jede 3. Zahl außer v. d. ersten 4 und letzten 5:", z[4:-5:3])
    
    # jede dritte Zahl aber davon nicht die ersten vier und nicht die letzten fünf
    # D.h. erst jede 3. Zahl aus der Liste, und HIERVON nicht die ersten 4 und letzten 5
    print("Jede 3. Zahl, aber davon nicht die ersten 4 und letzten 5:", z[::3][4:-5])

if __name__ == "__main__":
    main()
