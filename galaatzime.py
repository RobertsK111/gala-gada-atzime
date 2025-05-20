import pandas as pd
from statistics import mean

#Tiek nolasīs exel fails
df_raw = pd.read_excel("gala gada atzime.xlsx", sheet_name="Sheet1", skiprows=1)
df_raw = df_raw.rename(columns={
    "GALA VIDĒJĀ ATZĪME": "Priekšmets",
    "Unnamed: 2": "Komponents",
    "Unnamed: 4": "Svars(%)"
})
df_raw = df_raw.dropna(subset=["Priekšmets", "Komponents", "Svars(%)"])

# priekšmeti tiek sagrupēti pēc preikšmetiem
priekšmeti = df_raw["Priekšmets"].unique()

while True:
    print("\nIzvēlies kursu:")
    for i, pr in enumerate(priekšmeti, 1):
        print(f"{i}. {pr}")
    try:
        kursa_izvele = int(input("Tavs ievads: ")) - 1
        if kursa_izvele not in range(len(priekšmeti)):
            raise ValueError
    except ValueError:
        print("Nepareiza izvēle, mēģini vēlreiz.")
        continue

    izvēlētais_kurss = priekšmeti[kursa_izvele]
    dati = df_raw[df_raw["Priekšmets"] == izvēlētais_kurss].copy()

    komponentes = dati["Komponents"].tolist()
    ievadītie_dati = {}

    while len(ievadītie_dati) < len(komponentes):
        print("\nIzvēlies, kuru komponenti vēlies ievadīt:")
        atlikušās = [k for k in komponentes if k not in ievadītie_dati]
        for i, komp in enumerate(atlikušās, 1):
            print(f"{i}. {komp}")
        try:
            komp_izvele = int(input("Tavs ievads: ")) - 1
            izvēlētais_komponents = atlikušās[komp_izvele]
        except (ValueError, IndexError):
            print("Nepareiza izvēle.")
            continue

        try:
            atzīmes = list(map(int, input(f"Ievadi atzīmes priekš {izvēlētais_komponents} (atdalīt ar atstarpēm): ").split()))
            ievadītie_dati[izvēlētais_komponents] = atzīmes
        except ValueError:
            print("Nepareizs formāts.")
            continue

    gala_atzīme = 0.0
    for komp, atz in ievadītie_dati.items():
        vid = mean(atz)
        svars = dati.loc[dati["Komponents"] == komp, "Svars(%)"].values[0]
        gala_atzīme += vid * (svars / 100)

    print(f"\nTava gala gada atzīme priekš '{izvēlētais_kurss}': {round(gala_atzīme, 2)}")

    atkārtot = input("\nVai vēlies izvēlēties citu kursu? (ja/ne): ").strip().lower()
    if atkārtot != 'j':
        print("Programma beidzas.")
        break
