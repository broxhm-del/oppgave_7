# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 13:37:43 2025

@author: Bruker
"""

# DAT120 Øving 7 – Studieplan (grunnløsning)
# Krav dekket: meny 1–7 (obligatoriske) + litt ekstra validering
# Semestre: 1..6. 1/3/5 = Høst, 2/4/6 = Vår. Maks 30 sp per semester.

import json
from dataclasses import dataclass, asdict
from typing import Dict, List

# ---------- Modeller ----------

@dataclass
class Emne:
    kode: str
    navn: str
    sesong: str      # "høst" eller "vår"
    studiepoeng: int

# Alle emner (katalog), nøkkel = emnekode
emner: Dict[str, Emne] = {}

# Studieplan: dictionary fra semester (1..6) til liste av emnekoder
studieplan: Dict[int, List[str]] = {i: [] for i in range(1, 7)}

HOEST_SEM = {1, 3, 5}
VAAR_SEM = {2, 4, 6}

# ---------- Hjelpefunksjoner ----------

def sem_til_sesong(sem: int) -> str:
    if sem in HOEST_SEM:
        return "høst"
    if sem in VAAR_SEM:
        return "vår"
    return "ukjent"

def total_sp_i_semester(sem: int) -> int:
    return sum(emner[k].studiepoeng for k in studieplan[sem])

def skriv_emne(e: Emne) -> str:
    return f"{e.kode} – {e.navn} ({e.studiepoeng} sp, {e.sesong})"

def finnes_emne(kode: str) -> bool:
    return kode in emner

# ---------- Menyvalg (obligatoriske) ----------

def valg1_lag_emne():
    kode = input("Emnekode: ").strip().upper()
    if finnes_emne(kode):
        print("⚠️ Emnekode finnes allerede.")
        return
    navn = input("Navn: ").strip()
    sesong = input("Undervisningssesong (høst/vår): ").strip().lower()
    if sesong not in {"høst", "host", "vår", "var"}:
        print("⚠️ Skriv 'høst' eller 'vår'.")
        return
    if sesong == "host": sesong = "høst"
    if sesong == "var":  sesong = "vår"

    try:
        sp = int(input("Studiepoeng (heltall): ").strip())
        if sp <= 0:
            raise ValueError
    except ValueError:
        print("⚠️ Ugyldige studiepoeng.")
        return

    emner[kode] = Emne(kode, navn, sesong, sp)
    print("✅ Lagt til:", skriv_emne(emner[kode]))

def valg2_legg_til_emne_i_studieplan():
    if not emner:
        print("⚠️ Ingen emner registrert ennå.")
        return
    kode = input("Emnekode som skal legges i studieplan: ").strip().upper()
    if not finnes_emne(kode):
        print("⚠️ Emnekoden finnes ikke.")
        return
    try:
        sem = int(input("Semester (1–6): ").strip())
        if sem not in range(1, 7):
            raise ValueError
    except ValueError:
        print("⚠️ Ugyldig semester.")
        return

    forventet = sem_til_sesong(sem)
    if emner[kode].sesong != forventet:
        print(f"⚠️ Sesongfeil: {kode} undervises i {emner[kode].sesong}, "
              f"men semester {sem} er {forventet}.")
        return

    # sjekk 30-sp grense
    ny_sum = total_sp_i_semester(sem) + emner[kode].studiepoeng
    if ny_sum > 30:
        print(f"⚠️ For mange studiepoeng i semester {sem} ({ny_sum} > 30).")
        return

    if kode in studieplan[sem]:
        print("ℹ️ Emnet ligger allerede i dette semesteret.")
        return

    studieplan[sem].append(kode)
    print(f"✅ La {kode} i semester {sem}. Nå {ny_sum} sp i semesteret.")

def valg3_skriv_alle_emner():
    if not emner:
        print("ℹ️ Ingen emner registrert.")
        return
    print("\n📚 Alle registrerte emner:")
    for e in sorted(emnersom:=list(emner.values()), key=lambda x: x.kode):
        print(" -", skriv_emne(e))

def valg4_skriv_emner_per_semester():
    print()
    for sem in range(1, 7):
        ses = sem_til_sesong(sem)
        print(f"📆 Semester {sem} ({ses}) – {total_sp_i_semester(sem)} sp")
        if not studieplan[sem]:
            print("   (tomt)")
        else:
            for kode in studieplan[sem]:
                print("   -", skriv_emne(emner[kode]))

def valg5_sjekk_studieplan_gyldig():
    alt_ok = True
    print("\n🔎 Validering av studieplan:")
    for sem in range(1, 7):
        ses = sem_til_sesong(sem)
        sp = total_sp_i_semester(sem)
        if sp > 30:
            print(f"❌ Semester {sem}: {sp} sp (over 30).")
            alt_ok = False
        for kode in studieplan[sem]:
            if emner[kode].sesong != ses:
                print(f"❌ {kode} i sem {sem}: feil sesong ({emner[kode].sesong} ≠ {ses}).")
                alt_ok = False
    if alt_ok:
        print("✅ Studieplanen er gyldig.")

def valg6_lagre_til_fil():
    fil = input("Filnavn (f.eks. plan.json): ").strip()
    data = {
        "emner": {k: asdict(v) for k, v in emner.items()},
        "studieplan": studieplan
    }
    with open(fil, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 Lagret til {fil}")

def valg7_les_fra_fil():
    fil = input("Filnavn (f.eks. plan.json): ").strip()
    try:
        with open(fil, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("⚠️ Filen finnes ikke.")
        return
    except json.JSONDecodeError:
        print("⚠️ Ugyldig JSON-fil.")
        return

    emner.clear()
    for k, v in data.get("emner", {}).items():
        emner[k] = Emne(**v)
    # konverter nøkler til int hvis de ble lagret som str
    global studieplan
    studieplan = {int(k): list(v) for k, v in data.get("studieplan", {}).items()}
    print(f"📥 Leste {len(emner)} emner og studieplan fra {fil}")

# (Frivillig bonus) – enkel sletting av emne fra studieplan og/eller katalog
def bonus_slett_emne_fra_studieplan():
    try:
        sem = int(input("Semester (1–6): ").strip())
        if sem not in range(1, 7):
            raise ValueError
    except ValueError:
        print("⚠️ Ugyldig semester.")
        return
    kode = input("Emnekode som skal fjernes fra semesteret: ").strip().upper()
    if kode in studieplan[sem]:
        studieplan[sem].remove(kode)
        print(f"🗑️ Fjernet {kode} fra semester {sem}.")
    else:
        print("ℹ️ Emnet lå ikke i dette semesteret.")

# ---------- Meny ----------

def meny():
    while True:
        print("\n===== MENY =====")
        print("1) Lag et nytt emne")
        print("2) Legg et emne i studieplanen")
        print("3) Skriv ut liste over alle registrerte emner")
        print("4) Skriv ut studieplan (hvilke emner per semester)")
        print("5) Sjekk om studieplanen er gyldig")
        print("6) Lagre emnene og studieplanen til fil")
        print("7) Les inn emnene og studieplanen fra fil")
        print("8) Avslutt")
        print("(B) Bonus: Slett emne fra studieplan")
        valg = input("Valg: ").strip().lower()

        if valg == "1": valg1_lag_emne()
        elif valg == "2": valg2_legg_til_emne_i_studieplan()
        elif valg == "3": valg3_skriv_alle_emner()
        elif valg == "4": valg4_skriv_emner_per_semester()
        elif valg == "5": valg5_sjekk_studieplan_gyldig()
        elif valg == "6": valg6_lagre_til_fil()
        elif valg == "7": valg7_les_fra_fil()
        elif valg == "8": 
            print("👋 Avslutter.")
            break
        elif valg == "b":
            bonus_slett_emne_fra_studieplan()
        else:
            print("⚠️ Ugyldig valg.")

if __name__ == "__main__":
    meny()
