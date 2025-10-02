# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 13:42:08 2025

@author: sabri
"""

#1. sabrin - Lag et nytt emne
#2. ida - Legg til et emne i studieplanen
#3. hedda - Skriv ut ei liste over alle registrerte emner
#4. sabrin - Skriv ut studieplanen med hvilke emner som er i hvert semester
#5. ida - Sjekk om studieplanen er gyldig eller ikke

#lager ei fil som skal leses av i starten av programmet:
#6. Lagre emnene og studieplanen til fil
#7. Les inn emnene og studieplanen fra fil

def main():
    plan = Studieplan()

    while True:
        print("\nMeny:")
        print("1. Lag et nytt emne")
        print("2. Legg til et emne i studieplanen")
        print("3. Skriv ut alle registrerte emner")
        print("4. Skriv ut studieplan")
        print("5. Sjekk om studieplan er gyldig")
        print("6. Lagre emner og studieplan til fil (ikke implementert)")
        print("7. Les inn emner og studieplan fra fil (ikke implementert)")
        print("8. Avslutt")

        valg = input("Velg: ")

        if valg == "1":
            kode = input("Emnekode: ").upper()
            navn = input("Navn: ")
            sp = float(input("Studiepoeng: "))
            emne = Emne(kode, navn, sp)
            if #funksjon for oppg1:
                print("Emne lagt til.")
            else:
                print("Emne finnes allerede.")
      
        elif valg == "2":
            kode = input("Skriv inn emnekode: ").upper()
            sem = int(input("Semester (1-8): "))
            if #funksjon for oppg2:
                print("Emne lagt til i studieplan.")
            else:
                print("Kunne ikke legge til emnet.")
       
        elif valg == "3":
            print("Alle registrerte emner:")
            for e in #funksjon fra oppg3:
                print(" ", e)
      
        elif valg == "4":
            #funksjon fra oppg4:
      
        elif valg == "5":
            if #funksjon for oppg5:
                print("Studieplanen er gyldig.")
            else:
                print("Studieplanen er ikke gyldig (for mange studiepoeng i et semester).")

#usikker på fremgangsmåte og hva oppgaven spør etter:     
        elif valg == "6":
            print("Lagring til fil ikke implementert enda.")
      
        elif valg == "7":
            print("Lesing fra fil ikke implementert enda.")
     
        elif valg == "8":
            print("Avslutter...")
            break
        else:
            print("Ugyldig valg.")