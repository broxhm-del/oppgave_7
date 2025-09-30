# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 15:24:02 2025

@author: Bruker
"""
class Emne:
    def __init__(self, kode, navn, studiepoeng, anbefalt_semester=None):
        self.kode = kode
        self.navn = navn
        self.studiepoeng = studiepoeng
        self.anbefalt_semester = anbefalt_semester

    def __str__(self):
        return f"{self.kode} - {self.navn} ({self.studiepoeng} sp)"

class Studieplan:
    def __init__(self, antall_semestre=8):
        self.antall_semestre = antall_semestre
        self.semestre = {i: [] for i in range(1, antall_semestre + 1)}
        self.register = {}

    # --- Emneregister ---
    def legg_til_emne_i_register(self, emne):
        if emne.kode in self.register:
            return False
        self.register[emne.kode] = emne
        return True

    def alle_emner(self):
        return list(self.register.values())

    def hent_emne(self, kode):
        return self.register.get(kode)

    # --- Studieplan ---
    def legg_emne_i_semester(self, kode, semester):
        if kode not in self.register:
            return False
        if semester not in self.semestre:
            return False
        emne = self.register[kode]
        self.semestre[semester].append(emne)
        return True

    def skriv_ut_studieplan(self):
        for sem, emner in self.semestre.items():
            print(f"\nSemester {sem}:")
            if not emner:
                print("  (ingen emner)")
            for e in emner:
                print("  ", e)

    def er_gyldig(self):
        # Eksempel: ikke mer enn 30 sp per semester
        for sem, emner in self.semestre.items():
            total_sp = sum(e.studiepoeng for e in emner)
            if total_sp > 30:
                return False
        return True


# Meny
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
            if plan.legg_til_emne_i_register(emne):
                print("Emne lagt til.")
            else:
                print("Emne finnes allerede.")
        elif valg == "2":
            kode = input("Skriv inn emnekode: ").upper()
            sem = int(input("Semester (1-8): "))
            if plan.legg_emne_i_semester(kode, sem):
                print("Emne lagt til i studieplan.")
            else:
                print("Kunne ikke legge til emnet.")
        elif valg == "3":
            print("\nAlle registrerte emner:")
            for e in plan.alle_emner():
                print(" ", e)
        elif valg == "4":
            plan.skriv_ut_studieplan()
        elif valg == "5":
            if plan.er_gyldig():
                print("Studieplanen er gyldig.")
            else:
                print("Studieplanen er ikke gyldig (for mange studiepoeng i et semester).")
        elif valg == "6":
            print("Lagring til fil ikke implementert enda.")
        elif valg == "7":
            print("Lesing fra fil ikke implementert enda.")
        elif valg == "8":
            print("Avslutter...")
            break
        else:
            print("Ugyldig valg.")

if __name__ == "__main__":
    main()
