# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 17:34:22 2025

@author: sofiy
"""


antall_semestre = 6
semestre = {i: [] for i in range(1, antall_semestre + 1)}  # Hvert semester har en liste med emner
register = {}  # Emneregister: {kode: {"navn": navn, "studiepoeng": sp}}

#nytt - returnerer H for semestere som blir registrert som 1,3, eller 5
#og resten (2,4,6) blir returnert som V
def semester(sem):
    return "H" if sem in {1, 3, 5} else "V"

#nytt -summerer studiepoengene i et semester ved bruk av emnekodene som ligger
#i det semesteret
def studiepoeng(semestre, register, sem):
    return sum(register[k]["studiepoeng"] for k in semestre.get(sem, []))

# endret - bare bruk av ren logikk, ikke meny I/O (Input/Output)
#altså denne fikser reglene/logikken bak programmet som validering
#av emne - at emnekode ikke er tom eller allerede fins, eller at det ikke 
#står ugyldig tall for studiepoeng som f.eks et negativt tall etc.
def lag_emne(register):
    
    #Emnekode + validering
    while True:
        kode = input("Emnekode (f.eks. MAT100): ").strip().upper()
        if not kode:
            print("Error: Emnekode kan ikke være tom. Prøv igjen.")
            continue
        if kode in register:
            print("Error: Emnet finnes allerede. Prøv igjen.")
            continue
        break  # alt er ok
 

    # Navn + validering
    while True:
        navn = input("Navn på emnet: ").strip()
        if not navn:
            print("Error: Navn kan ikke være tomt. Prøv igjen.")
            continue
        break

    # Studiepoeng + validering, må være heltall > 0
    while True:
        studiepoeng = input("Studiepoeng (heltall > 0): ").strip()
        try:
            studiepoeng_int = int(studiepoeng)
            if studiepoeng_int <= 0:
                print("Error: Studiepoeng må være større enn 0. Prøv igjen.")
                continue
            break
        except ValueError:
           print("Error: Studiepoeng må være et heltall. Prøv igjen.")

    # Semester + validering
    while True:
        semester = input("Undervises emnet i Høst eller Vår? (H/V): ").strip().upper()
        if semester not in ("H", "V"):
            print("Error: Du må skrive H eller V. Prøv igjen.")
            continue
        break
    # Hvis alt er OK, lagre (NB: lagrer heltall, ikke tekst)
    register[kode] = {"navn": navn, "studiepoeng": studiepoeng_int, "semester": semester}
    print(f" Lagt til {navn} med emnekode {kode} ({'Høst' if semester=='H' else 'Vår'}, {studiepoeng_int} studiepoeng).")

#endre, legger et registrert emne inn i studieplanen - validerer alt i denen funksjonen
def legg_til_emne(semestre, register):

    # -Legg til emnekode + validering
    while True:
        kode = input("Hvilken emnekode vil du legge i planen? ").strip().upper()
        if not kode:
            print("Error: Emnekode kan ikke være tom. Prøv igjen.")
            continue
        if kode not in register:
            print("Error: Emnet finnes ikke i registeret. Legg det inn via valg 1 i menyen.")
            return
        # Emnet skal bare kunne legges til en gang i hele planen
        if any(kode in lst for lst in semestre.values()):
            print("Error: Emnet er allerede i studieplanen.")
            continue
        break

    # Semester + validering
    while True:
      s = input("Hvilket semester (1-6)? ").strip()
      try:
          s = int(s)
      except ValueError:
          print("Error: Semester må være et heltall 1–6. Prøv igjen.")
          continue

      if s not in semestre:  # bruker eksisterende 'semestre' liste øverst 
      # i filen som kilde til gyldige semestere
          print("Error: Semester må være 1–6. Prøv igjen.")
          continue

      # Høst eller Vår: emnets lagrede H/V må matche semestertype for s
      hv_emne = register[kode]["semester"]
      hv_sem  = semester(s)
      if hv_emne != hv_sem:
         print(f"Error: {kode} er et {'høst' if hv_emne == 'H' else 'vår'}-emne og kan bare legges i {'1, 3, 5' if hv_emne == 'H' else '2, 4, 6'}.")
         continue

      # 30 SP-grense- bruker studiepoeng() + emnets studiepoeng fra registeret
      if studiepoeng(semestre, register, s) + register[kode]["studiepoeng"] > 30:
          print(f"Error: Dette gir over 30 studiepoeng i semester {s}.")
          continue

      # Hvis alt er OK legg inn emnet i studieplanen
      semestre[s].append(kode)
      print(f" La {kode} i semester {s}. (Ny studiepoeng sum for semesteret: {studiepoeng(semestre, register, s)} SP)")
      break


# Skriver ut ei liste over alle registrerte emner
# Bruker register som inneholder emnekode, navn, studiepoeng og H/V
def skriv_ut_alle_emner(register):
    # Sjekker først om det finnes noen emner
    if not register:
        print("Ingen emner registrert enda.")
        return
    
    print("Alle registrerte emner:")
    # Går gjennom hvert emne i registeret og skriver ut informasjon
    for kode, info in register.items():
        hv = "Høst" if info["semester"] == "H" else "Vår"
        print(f" - {kode}: {info['navn']} ({info['studiepoeng']} studiepoeng, {hv})")


# Skriver ut studieplanen med hvilke emner som ligger i hvert semester
# Bruker semester()-funksjonen for å vise om semesteret er høst eller vår
def skriv_ut_studieplan(semestre, register, antall_semestre=6):
    print("STUDIEPLAN:")
    # Løkke gjennom alle 6 semestre
    for s in range(1, antall_semestre + 1):
        hv_txt = "Høst" if semester(s) == "H" else "Vår"
        sp_sum = studiepoeng(semestre, register, s)
        print(f"Semester {s} ({hv_txt}) – {sp_sum} studiepoeng")
        
        # Hvis semesteret er tomt
        if not semestre[s]:
            print("   (tomt)")
            
        else:
            # Skriver ut alle emner som ligger i semesteret
            for k in semestre[s]:
                info = register.get(k)
                if info is None:
                    print(f"   {k}: (mangler i registeret)")
                else:
                    hv_emne = "Høst" if info["semester"] == "H" else "Vår"
                    print(f"   {k}: {info['navn']} ({info['studiepoeng']} studiepoeng, {hv_emne})")


# Sjekker om studieplanen er gyldig
# Et semester er bare gyldig hvis det inneholder nøyaktig 30 studiepoeng
# Sjekk om studieplanen er gyldig (30 SP i hvert semester) – KORT VERSJON
def sjekk_gyldig_studieplan(semestre, register, antall_semestre=6):
    gyldige = []
    ugyldige = []

    for s in range(1, antall_semestre + 1):
        sp_sum = studiepoeng(semestre, register, s)
        if sp_sum == 30:
            gyldige.append(s)
        else:
            ugyldige.append((s, sp_sum))

    if gyldige:
        print("Gyldige semestre (30 studiepoeng): " + ", ".join(str(s) for s in gyldige))
        for s in gyldige:                            
            print(f" - Semester {s}: 30 studiepoeng") 
            
    if ugyldige:
        print("Ugyldige semestre (≠ 30 studiepoeng): " + ", ".join(str(s) for s, _ in ugyldige))
        for s, sp_sum in ugyldige:
            print(f" - Semester {s}: {sp_sum} studiepoeng")
    

def pause():
    input(" (Trykk Enter for å gå tilbake til menyen) ")

def main():

    while True:
        print("Meny:")
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
                lag_emne(register); pause()
                
        elif valg == "2":
                legg_til_emne(semestre, register); pause()
                
        elif valg == "3":
            skriv_ut_alle_emner(register); pause()
            
        elif valg == "4":
            skriv_ut_studieplan(semestre, register); pause()
            
        elif valg == "5":
            sjekk_gyldig_studieplan(semestre, register); pause()
        else:
            print("Ugyldig valg.")
            
#Kjører programmet            
if __name__ == "__main__":
    main()
