# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 13:37:43 2025

@author: Bruker
"""
Dette blir bra
# DAT120 øving 7 – enkel løsning uten json/dataclass
# Lagrer til/leser fra en enkel tekstfil plan.txt

# ---------- Data ----------
# Alle emner: {kode: {"navn": str, "sesong": "høst"/"vår", "sp": int}}
emner = {}

# Studieplan: {semester(1..6): [emnekoder]}
studieplan = {i: [] for i in range(1, 7)}

# ---------- Hjelpefunksjoner ----------
def sem_sesong(sem):
    return "høst" if sem % 2 == 1 else "vår"

def sp_sum(sem):
    return sum(emner[k]["sp"] for k in studieplan[sem])

def input_int(tekst):
    try:
        return int(input(tekst).strip())
    except ValueError:
        return None

# ---------- Menyvalg ----------
def valg1_lag_emne()
    kode = input("Emnekode: ").strip().upper()
    if not kode:
        print("⚠️ Emnekode kan ikke være tom.")
        return
    if kode in emner:
        print("⚠️ Emnekoden finnes allerede.")
        return

    navn = input("Navn: ").strip()
    sesong = input("Undervisning (høst/vår): ").strip().lower()
    if sesong == "host": sesong = "høst"   # tillat uten ø
    if sesong == "var":  sesong = "vår"

    sp = input_int("Studiepoeng (heltall): ")
    if not navn or sesong not in {"høst", "vår"} or not isinstance(sp, int) or sp <= 0:
        print("⚠️ Ugyldig input.")
        return

    emner[kode] = {"navn": navn, "sesong": sesong, "sp": sp}
    print(f"✅ Lagt til {kode} – {navn} ({sp} sp, {sesong})")

def valg2_legg_til_i_studieplan():
    if not emner:
        print("⚠️ Ingen emner registrert ennå.")
        return
    kode = input("Emnekode som skal legges i studieplan: ").strip().upper()
    if kode not in emner:
        print("⚠️ Emnet finnes ikke.")
        return
    sem = input_int("Semester (1–6): ")
    if sem not in range(1, 7):
        print("⚠️ Ugyldig semester.")
        return

    # Sesong og 30-sp-regel
    forventet = sem_sesong(sem)
    if emner[kode]["sesong"] != forventet:
        print(f"⚠️ Feil sesong: {kode} er {emner[kode]['sesong']}, men semester {sem} er {forventet}.")
        return
    if sp_sum(sem) + emnersp := emner[kode]["sp"] > 30:  # walrus forenker litt
        print(f"⚠️ For mye studiepoeng i sem {sem} (ville blitt {sp_sum(sem) + emnersp}).")
        return
    if kode in studieplan[sem]:
        print("ℹ️ Emnet ligger allerede i dette semesteret.")
        return

    studieplan[sem].append(kode)
    print(f"✅ La {kode} i semester {sem}. Nå {sp_sum(sem)} sp i semesteret.")

def valg3_skriv_alle_emner():
    if not emner:
        print("ℹ️ Ingen emner registrert.")
        return
    print("\n📚 Alle emner:")
    for kode in sorted(emner):
        e = emner[kode]
        print(f" - {kode} – {e['navn']} ({e['sp']} sp, {e['sesong']})")

def valg4_skriv_studieplan():
    print()
    for sem in range(1, 7):
        print(f"Semester {sem} ({sem_sesong(sem)}), {sp_sum(sem)} sp")
        if not studieplan[sem]:
            print("  (tomt)")
        else:
            for kode in studieplan[sem]:
                e = emner[kode]
                print(f"  - {kode} – {e['navn']} ({e['sp']} sp)")

def valg5_sjekk_gyldighet():
    alt_ok = True
    for sem in range(1, 7):
        # 30 sp-regel
        if sp_sum(sem) > 30:
            print(f"❌ Semester {sem} har {sp_sum(sem)} sp (over 30).")
            alt_ok = False
        # riktig sesong
        forventet = sem_sesong(sem)
        for kode in studieplan[sem]:
            if emner[kode]["sesong"] != forventet:
                print(f"❌ {kode} feil sesong i semester {sem} ({emner[kode]['sesong']} ≠ {forventet}).")
                alt_ok = False
    print("✅ Studieplanen er gyldig." if alt_ok else "⚠️ Studieplanen er ikke gyldig.")

def valg6_lagre_til_fil():
    # ÉN enkel tekstfil med to seksjoner
    # [EMNER]
    # KODE;NAVN;SESONG;SP
    # [PLAN]
    # SEM: KODE1,KODE2,...
    filnavn = input("Filnavn (standard: plan.txt): ").strip() or "plan.txt"
    try:
        with open(filnavn, "w", encoding="utf-8") as f:
            f.write("[EMNER]\n")
            for kode in sorted(emner):
                e = emner[kode]
                # Bytt ut evt. semikolon i navn for robusthet
                navn = e["navn"].replace(";", ",")
                f.write(f"{kode};{navn};{e['sesong']};{e['sp']}\n")
            f.write("[PLAN]\n")
            for sem in range(1, 7):
                f.write(f"{sem}: {','.join(studieplan[sem])}\n")
        print(f"💾 Lagret til {filnavn}")
    except Exception as ex:
        print("⚠️ Klarte ikke lagre:", ex)

def valg7_les_fra_fil():
    filnavn = input("Filnavn (standard: plan.txt): ").strip() or "plan.txt"
    try:
        with open(filnavn, "r", encoding="utf-8") as f:
            modus = None
            # tøm nåværende data
            emner.clear()
            for sem in range(1, 7):
                studieplan[sem].clear()

            for rå in f:
                linje = rå.strip()
                if not linje:
                    continue
                if linje == "[EMNER]":
                    modus = "EMNER"; continue
                if linje == "[PLAN]":
                    modus = "PLAN"; continue
                if modus == "EMNER":
                    # KODE;NAVN;SESONG;SP
                    deler = linje.split(";")
                    if len(deler) != 4: 
                        continue
                    kode, navn, sesong, sp = deler
                    emner[kode] = {"navn": navn, "sesong": sesong, "sp": int(sp)}
                elif modus == "PLAN":
                    # SEM: K1,K2,K3
                    if ":" not in linje: 
                        continue
                    venstre, høyre = linje.split(":", 1)
                    try:
                        sem = int(venstre.strip())
                        koder = [k.strip() for k in høyre.split(",") if k.strip()]
                        studieplan[sem] = koder
                    except:
                        pass
        print(f"📥 Lest fra {filnavn}")
    except FileNotFoundError:
        print("⚠️ Fant ikke filen.")
    except Exception as ex:
        print("⚠️ Klarte ikke lese fil:", ex)

# ---------- Meny ----------
def meny():
    while True:
        print("\n1) Lag nytt emne")
        print("2) Legg til emne i studieplan")
        print("3) Skriv ut alle registrerte emner")
        print("4) Skriv ut studieplan per semester")
        print("5) Sjekk om studieplanen er gyldig")
        print("6) Lagre til fil")
        print("7) Les fra fil")
        print("0) Avslutt")
        v = input("Valg: ").strip()
        if v == "1": valg1_lag_emne()
        elif v == "2": valg2_legg_til_i_studieplan()
        elif v == "3": valg3_skriv_alle_emner()
        elif v == "4": valg4_skriv_studieplan()
        elif v == "5": valg5_sjekk_gyldighet()
        elif v == "6": valg6_lagre_til_fil()
        elif v == "7": valg7_les_fra_fil()
        elif v == "0": 
            print("👋 Avslutter."); break
        else:
            print("Ugyldig valg.")

if __name__ == "__main__":
    meny()

