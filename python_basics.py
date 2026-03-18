# ==========================================
# Python Basics Tutorial AI
# ==========================================

# 1. Ausgabe (Output)
# 'print' gibt Text in der Konsole aus.
print("Hallo! Willkommen zum Python-Basics Tutorial.")
print("------------------------------------------")

# 2. Variablen und Datentypen
# Variablen speichern Daten. Python erkennt den Typ automatisch.
name = "Python-Lerner"     # String (Text)
alter = 25                 # Integer (Ganze Zahl)
koerpergroesse = 1.75      # Float (Kommazahl)
ist_motiviert = True       # Boolean (Wahrheitswert: True oder False)

# f-Strings ermöglichen es, Variablen direkt in den Text einzufügen
print(f"Name: {name}, Alter: {alter}, Motiviert: {ist_motiviert}")

# 3. Listen (Arrays)
# Listen speichern mehrere Werte in einer geordneten Reihenfolge.
fruechte = ["Apfel", "Banane", "Orange"]
print(f"\nMeine Lieblingsfrucht ist {fruechte[0]}") # Achtung: Zählung beginnt bei 0!

fruechte.append("Traube") # Ein neues Element am Ende hinzufügen
print(f"Alle Früchte: {fruechte}")

# 4. Dictionaries (Wörterbücher)
# Speichern Daten in Schlüssel-Wert-Paaren (Key-Value)
person = {
    "name": "Max",
    "alter": 30,
    "stadt": "Berlin"
}
print(f"\n{person['name']} kommt aus {person['stadt']}.")

# 5. if-else Bedingungen (Kontrollstrukturen)
# Ermöglicht Entscheidungen im Code
print("\n--- Altersprüfung ---")
if alter >= 18:
    print("Du bist volljährig.")
elif alter == 17:
    print("Fast volljährig!")
else:
    print("Du bist minderjährig.")

# 6. Schleifen (Loops)
print("\n--- For-Schleife ---")
# Führt Code für jedes Element in einer Liste (oder einem anderen durchlaufbaren Objekt) aus
for frucht in fruechte:
    print(f"Ich esse gerne {frucht}")

print("\n--- While-Schleife ---")
# Wiederholt den Code, solange eine bestimmte Bedingung wahr (True) ist
counter = 0
while counter < 3:
    print(f"Zähler ist bei: {counter}")
    counter += 1 # Kurzform für: counter = counter + 1

# 7. Funktionen
print("\n--- Funktionen ---")
# Funktionen bündeln Code-Blöcke, um sie später einfach wiederzuverwenden (vermeidet Wiederholungen)
def begruesse(name_der_person):
    """Diese Funktion nimmt einen Namen und gibt eine Begrüßung zurück."""
    return f"Hallo {name_der_person}, schön, dass du programmieren lernst!"

# Aufruf der Funktion
nachricht1 = begruesse("Anna")
nachricht2 = begruesse("Tom")

print(nachricht1)
print(nachricht2)

print("\n------------------------------------------")
print("Das waren die wichtigsten Basics! Spiel gerne mit dem Code herum.")
