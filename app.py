import streamlit as st
import pandas as pd
import os
import numpy as np

# Régression simple sans sklearn
if len(data) > 1:
    x = data["Heures_Etude"]
    y = data["Note"]

    # calcul manuel (moindres carrés)
    a = np.cov(x, y)[0][1] / np.var(x)
    b = y.mean() - a * x.mean()

    prediction = a * 5 + b

    st.write(f"📌 Note prédite pour 5h d'étude : {prediction:.2f}")

st.set_page_config(page_title="Analyse des données", layout="centered")

st.title("📊 Application de collecte et analyse des données")

# Fichier de stockage
FILE = "data.csv"

# Création du fichier s'il n'existe pas
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["Nom", "Age", "Sexe", "Heures_Etude", "Note"])
    df.to_csv(FILE, index=False)

# Charger les données
data = pd.read_csv(FILE)

# ==============================
# 🔹 1. Collecte de données
# ==============================
st.header("📝 Collecte des données")

nom = st.text_input("Nom")
age = st.number_input("Âge", min_value=10, max_value=100)
sexe = st.selectbox("Sexe", ["Homme", "Femme"])
heures = st.number_input("Heures d'étude par jour", min_value=0.0, step=0.5)
note = st.number_input("Note obtenue", min_value=0.0, max_value=20.0)

if st.button("Enregistrer"):
    new_data = pd.DataFrame([[nom, age, sexe, heures, note]],
                            columns=data.columns)
    new_data.to_csv(FILE, mode='a', header=False, index=False)
    st.success("✅ Donnée enregistrée !")

# ==============================
# 🔹 2. Affichage des données
# ==============================
st.header("📋 Données collectées")
data = pd.read_csv(FILE)
st.dataframe(data)

# ==============================
# 🔹 3. Analyse descriptive
# ==============================
st.header("📈 Analyse descriptive")

if not data.empty:
    st.write("Statistiques :")
    st.write(data.describe())

    st.subheader("Distribution des notes")
    st.bar_chart(data["Note"])

    st.subheader("Heures d'étude vs Note")
    st.scatter_chart(data[["Heures_Etude", "Note"]])

# ==============================
# 🔹 4. Régression linéaire
# ==============================
st.header("📉 Régression linéaire")

if len(data) > 1:
    X = data[["Heures_Etude"]]
    y = data["Note"]

    model = LinearRegression()
    model.fit(X, y)

    prediction = model.predict([[5]])  # exemple 5h d'étude

    st.write(f"📌 Note prédite pour 5h d'étude : {prediction[0]:.2f}")

# ==============================
# 🔹 5. Classification simple
# ==============================
st.header("📊 Classification")

if not data.empty:
    data["Niveau"] = data["Note"].apply(lambda x: "Faible" if x < 10 else "Bon")
    st.write(data[["Nom", "Note", "Niveau"]])