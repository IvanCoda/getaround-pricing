import pandas as pd

# Charger le fichier Excel
delay_df = pd.read_excel("/content/get_around_delay_analysis.xlsx")

# On ne garde que les locations terminées
ended_df = delay_df[delay_df["state"] == "ended"].copy()

# Supprimer les lignes sans info sur le délai
ended_df = ended_df[ended_df["delay_at_checkout_in_minutes"].notna()]

# Fonction de classification des retards
def categorize_delay(delay):
    if delay <= 0:
        return "on_time_or_early"
    elif delay <= 15:
        return "0-15 min"
    elif delay <= 30:
        return "15-30 min"
    elif delay <= 60:
        return "30-60 min"
    else:
        return "60+ min"

# Appliquer la fonction à la colonne des retards
ended_df["delay_category"] = ended_df["delay_at_checkout_in_minutes"].apply(categorize_delay)


# Regrouper par type de check-in et catégorie de retard
delay_distribution = ended_df.groupby(["checkin_type", "delay_category"]).size().unstack(fill_value=0)

# Afficher le tableau de distribution
print(delay_distribution)


import matplotlib.pyplot as plt

delay_distribution.T.plot(kind="bar", figsize=(10, 6))
plt.title("Distribution des retards par type de check-in")
plt.xlabel("Catégorie de retard")
plt.ylabel("Nombre de locations")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.tight_layout()
plt.show()


# On conserve les lignes avec une location précédente et un delta de temps
relevant_df = ended_df[ended_df["time_delta_with_previous_rental_in_minutes"].notna()].copy()


# Définir les seuils à tester
seuils = [15, 30, 45, 60, 90]
results = []

# Boucle sur les seuils et types de checkin
for seuil in seuils:
    for checkin_type in ["connect", "mobile"]:
        df_type = relevant_df[relevant_df["checkin_type"] == checkin_type]

        # Identifier les cas problématiques : retard + délai trop court
        cas_problematique = df_type[
            (df_type["delay_at_checkout_in_minutes"] > 0) &
            (df_type["time_delta_with_previous_rental_in_minutes"] < seuil)
        ]

        results.append({
            "checkin_type": checkin_type,
            "seuil_min (minutes)": seuil,
            "cas_possibles": len(df_type),
            "cas_problématiques": len(cas_problematique),
            "proportion_problématique (%)": round(100 * len(cas_problematique) / len(df_type), 2)
        })

# Résultats sous forme de tableau
seuils_df = pd.DataFrame(results)

# Affichage
print(seuils_df)


