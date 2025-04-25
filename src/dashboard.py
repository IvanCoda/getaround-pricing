import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 🔁 Chargement des données
delay_df = pd.read_excel("get_around_delay_analysis.xlsx")
pricing_df = pd.read_csv("get_around_pricing_project.csv")

# ⚙️ Prétraitement des données
df = delay_df[delay_df["state"] == "ended"].copy()
df = df[df["delay_at_checkout_in_minutes"].notna()]
df = df[df["time_delta_with_previous_rental_in_minutes"].notna()]

# 💶 Prix moyen journalier
prix_moyen_journalier = pricing_df["rental_price_per_day"].mean()

# 🖼️ Interface
st.title("🚗 Getaround - Dashboard des Retards de Location")

seuil = st.slider("⏱️ Choisissez un seuil de délai minimum (minutes)", 0, 120, 30, step=30)
checkin_type = st.selectbox("🔌 Type de check-in", ["tous", "connect", "mobile"])

# 🧹 Filtrage
if checkin_type != "tous":
    df = df[df["checkin_type"] == checkin_type]

# ⚠️ Cas problématiques
df_probleme = df[
    (df["delay_at_checkout_in_minutes"] > 0) &
    (df["time_delta_with_previous_rental_in_minutes"] < seuil)
]

# 🔢 Statistiques
st.subheader("📊 Résultats")
st.markdown(f"- Nombre total de cas analysés : `{len(df)}`")
st.markdown(f"- Nombre de cas problématiques : `{len(df_probleme)}`")
st.markdown(f"- Pourcentage impacté : `{round(100 * len(df_probleme) / len(df), 2)} %`")

# 💸 Estimation du manque à gagner
perte_estimee = len(df_probleme) * prix_moyen_journalier

st.subheader("💸 Estimation du manque à gagner")
st.markdown(
    f"Si l'on applique un seuil de `{seuil} min` "
    f"sur les locations `{checkin_type}`, on éviterait `{len(df_probleme)}` cas problématiques."
)
st.markdown(
    f"Le manque à gagner estimé serait d’environ **{round(perte_estimee):,} €**, "
    f"en supposant qu'une location est perdue pour chaque cas critique."
)

# 📈 Graphique Seuil vs Perte estimée
seuils = range(0, 121, 30)
pertes = []

for s in seuils:
    temp_df = df[
        (df["delay_at_checkout_in_minutes"] > 0) &
        (df["time_delta_with_previous_rental_in_minutes"] < s)
    ]
    pertes.append(len(temp_df) * prix_moyen_journalier)

st.subheader("📉 Perte estimée selon le seuil choisi")
fig, ax = plt.subplots()
ax.plot(seuils, pertes, marker='o')
ax.set_title("Seuil vs Perte estimée (€)")
ax.set_xlabel("Seuil (minutes)")
ax.set_ylabel("Perte (€)")
st.pyplot(fig)

# 🧠 Recommandation
st.subheader("🧠 Recommandation")

seuil_reco = None
for s, p in zip(seuils, pertes):
    taux = 100 * p / (len(df) * prix_moyen_journalier)
    if taux <= 5:
        seuil_reco = s
        break

if seuil_reco:
    st.success(
        f"💡 En appliquant un **seuil de {seuil_reco} minutes**, "
        f"on limite les conflits tout en gardant la perte sous **5%** du revenu potentiel."
    )
else:
    st.warning(
        "Aucun seuil ne permet de rester sous 5% de perte estimée. "
        "Réduire la durée moyenne des retards pourrait être envisagé en priorité."
    )

# 📋 Données brutes
if st.checkbox("Afficher les données brutes des cas problématiques"):
    st.write(df_probleme)
