# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 12:52:03 2025

@author: Bruker
"""
import json


def hv(sem):
    """Returner 'H' for 1,3,5 og 'V' for 2,4,6."""
    return 'H' if sem in (1, 3, 5) else 'V'

# Domene-klasser

class Emne:
    def __init__(self, kode, navn, sp, semester_hv):
        self.kode = kode.upper().strip()
        self.navn = navn.strip()
        self.sp = int(sp)
        self.semester = semester_hv.upper().strip()  # 'H' eller 'V'

    def som_dict(self):
        return {"emnekode": self.kode, "navn": self.navn, "studiepoeng": self.sp, "semester": self.semester}

    @staticmethod
    def fra_dict(d):
        return Emne(d["emnekode"], d["navn"], d["studiepoeng"], d["semester"])


class Studieplan:
    def __init__(self, plan_id, tittel, antall_semestre=6):
        self.id = plan_id
        self.tittel = tittel
        # Hvert semester er en liste med Emne-objekter
        self.semestre = {i: [] for i in range(1, antall_semestre + 1)}

    def total_sp(self, s):
        return sum(e.sp for e in self.semestre[s])

    def inneholder(self, emnekode):
        k = emnekode.upper()
        return any(any(e.kode == k for e in lst) for lst in self.semestre.values())

    def legg_til(self, emne, s):
        if s not in self.semestre:
            print("Semester må være 1–6."); return
        if emne.semester != hv(s):
            print("Feil semester-typematch (H/V)."); return
        if self.inneholder(emne.kode):
            print("Emnet finnes allerede i planen."); return
        if self.total_sp(s) + emne.sp > 30:
            print(f"Over 30 studiepoeng i semester {s}."); return
        self.semestre[s].append(emne)
        print(f"La {emne.kode} i semester {s}.")

    def fjern(self, emnekode):
        k = emnekode.upper()
        for s in self.semestre:
            for i, e in enumerate(self.semestre[s]):
                if e.kode == k:
                    del self.semestre[s][i]
                    print(f"Fjernet {k} fra semester {s}.")
                    return True
        print("Emnet finnes ikke i denne planen.")
        return False

    def skriv_ut(self):
        print(f"\nSTUDIEPLAN – {self.tittel} (id={self.id})")
        for s in range(1, 7):
            hv_txt = "Høst" if hv(s) == 'H' else "Vår"
            print(f"Semester {s} ({hv_txt}) – {self.total_sp(s)} studiepoeng")
            if not self.semestre[s]:
                print("  (tomt)")
            else:
                for e in self.semestre[s]:
                    hv_e = "Høst" if e.semester == 'H' else "Vår"
                    print(f"  {e.kode}: {e.navn} ({e.sp} sp, {hv_e})")

    def gyldighetsrapport(self):
        gyldige, ugyldige = [], []
        for s in range(1, 7):
            sps = self.total_sp(s)
            (gyldige if sps == 30 else ugyldige).append((s, sps))
        return gyldige, ugyldige

    def som_dict(self):
        # lagre emner i semester som emnekoder (enkelt JSON-format)
        return {"id": self.id, "tittel": self.tittel, "semestre": {s: [e.kode for e in lst] for s, lst in self.semestre.items()}}

    @staticmethod
    def fra_dict(d, emneregister):
        sp = Studieplan(d["id"], d["tittel"])
        for s_str, koder in d.get("semestre", {}).items():
            s = int(s_str)
            for k in koder:
                e = emneregister.get(k)
                if e:
                    # Bruk min-rulett: enkel validering ved innlasting
                    if hv(s) == e.semester and sp.total_sp(s) + e.sp <= 30:
                        sp.semestre[s].append(e)
        return sp


# Enkle "databaser" i minne

EMNER = {}        # {"DAT120": Emne(...)}
STUDIEPLANER = {} # {"INF01": Studieplan(...)}
FIL = "studieplaner.json"

# Lagring / lesing

def lagre():
    data = {
        "emner": {k: e.som_dict() for k, e in EMNER.items()},
        "studieplaner": {pid: p.som_dict() for pid, p in STUDIEPLANER.items()},
    }
    try:
        with open(FIL, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Lagret til '{FIL}'.")
    except Exception as e:
        print("Feil ved lagring:", e)


def les():
    global EMNER, STUDIEPLANER
    try:
        with open(FIL, "r", encoding="utf-8") as f:
            data = json.load(f)
        EMNER = {k: Emne.fra_dict(v) for k, v in data.get("emner", {}).items()}
        STUDIEPLANER = {}
        for pid, pd in data.get("studieplaner", {}).items():
            STUDIEPLANER[pid] = Studieplan.fra_dict(pd, EMNER)
        print(f"Lest fra '{FIL}'.")
    except FileNotFoundError:
        print(f"Fant ikke '{FIL}'. Lagre først.")
    except Exception as e:
        print("Feil ved lesing:", e)

# Interaktiv meny

def pause():
    input("(Enter for meny)")

def velg_plan():
    if not STUDIEPLANER:
        print("Ingen studieplaner. Lag en med valg 5.")
        return None
    print("Tilgjengelige planer:")
    for pid, p in STUDIEPLANER.items():
        print(f" - {pid}: {p.tittel}")
    pid = input("Velg plan-id: ").strip()
    return STUDIEPLANER.get(pid)

# 1. Lag et nytt emne

def v1():
    kode = input("Emnekode (f.eks. DAT120): ").strip().upper()
    if not kode or kode in EMNER:
        print("Ugyldig eller finnes allerede."); return
    navn = input("Navn: ").strip()
    try:
        sp = int(input("Studiepoeng: ").strip())
    except ValueError:
        print("Må være heltall."); return
    hv_in = input("Semester (H/V): ").strip().upper()
    if hv_in not in ("H","V"):
        print("Skriv H eller V."); return
    EMNER[kode] = Emne(kode, navn, sp, hv_in)
    print("Lagt til", kode)

# 2. Legg til et emne i en studieplan

def v2():
    p = velg_plan();  
    if not p: return
    kode = input("Emnekode som skal legges til: ").strip().upper()
    e = EMNER.get(kode)
    if not e:
        print("Emne finnes ikke. Lag det først (valg 1)."); return
    try:
        s = int(input("Semester (1–6): ").strip())
    except ValueError:
        print("Må være heltall 1–6."); return
    p.legg_til(e, s)

# 3. Fjern et emne fra en studieplan

def v3():
    p = velg_plan();  
    if not p: return
    kode = input("Emnekode som skal fjernes: ").strip().upper()
    p.fjern(kode)

# 4. Skriv ut alle registrerte emner

def v4():
    if not EMNER:
        print("Ingen emner registrert."); return
    print("Alle emner:")
    for k, e in EMNER.items():
        print(f" - {e.kode}: {e.navn} ({e.sp} sp, {'Høst' if e.semester=='H' else 'Vår'})")

# 5. Lag en ny tom studieplan

def v5():
    pid = input("Ny plan-id: ").strip()
    if not pid or pid in STUDIEPLANER:
        print("Ugyldig eller finnes allerede."); return
    tittel = input("Tittel: ").strip()
    STUDIEPLANER[pid] = Studieplan(pid, tittel)
    print("Opprettet plan", pid)

# 6. Skriv ut en studieplan

def v6():
    p = velg_plan();  
    if p: p.skriv_ut()

# 7. Sjekk om en studieplan er gyldig

def v7():
    p = velg_plan();  
    if not p: return
    gyldige, ugyldige = p.gyldighetsrapport()
    if gyldige:
        print("Gyldige semestre (30 sp):", ", ".join(str(s) for s, _ in gyldige))
    if ugyldige:
        print("Ugyldige semestre (≠ 30 sp):")
        for s, sp_sum in ugyldige:
            print(f" - Semester {s}: {sp_sum} sp")

# 8. Finn hvilke studieplaner som bruker et emne

def v8():
    kode = input("Emnekode: ").strip().upper()
    funn = [p.tittel for p in STUDIEPLANER.values() if p.inneholder(kode)]
    if funn:
        print("Brukes i:")
        for t in funn: print(" -", t)
    else:
        print("Ingen planer bruker dette emnet.")

# 9. Lagre

def v9():
    lagre()

# 10. Les

def v10():
    les()

# 11. Avslutt

# Program-loop


def meny():
    print("\nMeny:")
    print("1. Lag et nytt emne")
    print("2. Legg til et emne i en studieplan")
    print("3. Fjern et emne fra en studieplan")
    print("4. Skriv ut ei liste over alle registrerte emner")
    print("5. Lag en ny tom studieplan")
    print("6. Skriv ut en studieplan med hvilke emner som er i hvert semester")
    print("7. Sjekk om en studieplan er gyldig eller ikke")
    print("8. Finn hvilke studieplaner som bruker et oppgitt emne")
    print("9. Lagre emnene og studieplanene til fil")
    print("10. Les inn emnene og studieplanene fra fil")
    print("11. Avslutt")


def main():
    while True:
        meny()
        valg = input("Velg: ").strip()
        if valg == "1": v1(); pause()
        elif valg == "2": v2(); pause()
        elif valg == "3": v3(); pause()
        elif valg == "4": v4(); pause()
        elif valg == "5": v5(); pause()
        elif valg == "6": v6(); pause()
        elif valg == "7": v7(); pause()
        elif valg == "8": v8(); pause()
        elif valg == "9": v9(); pause()
        elif valg == "10": v10(); pause()
        elif valg == "11":
            print("Avslutter. Ha en fin dag!")
            break
        else:
            print("Ugyldig valg.")

if __name__ == "__main__":
    main()
