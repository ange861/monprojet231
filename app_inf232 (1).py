"""
INF 232 EC2 - Application de Collecte et Analyse Descriptive des Donnees
Secteur : Sante et Epidemiologie Communautaire
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import datetime
import os

# ─────────────────────────────────────────────
#  CONFIGURATION DE LA PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DataSante 232 | Collecte et Analyse",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS PERSONNALISE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
}

.main-header {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
}

.main-header h1 {
    color: #00e5ff !important;
    font-size: 2.4rem;
    margin-bottom: 0.3rem;
}

.main-header p {
    color: #b0bec5;
    font-size: 1rem;
}

.metric-card {
    background: linear-gradient(135deg, #1a237e, #283593);
    color: white;
    padding: 1.2rem;
    border-radius: 12px;
    text-align: center;
    border-left: 4px solid #00e5ff;
}

.metric-card h2 {
    font-size: 2rem !important;
    color: #00e5ff !important;
    margin: 0;
}

.metric-card p {
    color: #90caf9;
    margin: 0;
    font-size: 0.85rem;
}

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #0d47a1;
    border-bottom: 3px solid #00e5ff;
    padding-bottom: 0.4rem;
    margin-bottom: 1.2rem;
}

.success-box {
    background: #e8f5e9;
    border-left: 4px solid #43a047;
    padding: 0.8rem 1.2rem;
    border-radius: 8px;
    color: #2e7d32;
    font-weight: 500;
}

.info-box {
    background: #e3f2fd;
    border-left: 4px solid #1976d2;
    padding: 0.8rem 1.2rem;
    border-radius: 8px;
    color: #0d47a1;
}

.stButton > button {
    background: linear-gradient(135deg, #0d47a1, #1565c0);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1565c0, #1976d2);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(13,71,161,0.4);
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE ET PERSISTANCE
# ─────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame()

DATA_FILE = "donnees_sante.csv"

def charger_donnees():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame()

def sauvegarder_donnees(df):
    df.to_csv(DATA_FILE, index=False)

if st.session_state.data.empty:
    st.session_state.data = charger_donnees()

# ─────────────────────────────────────────────
#  BARRE DE NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <h2 style='color:#0d47a1; margin:0.3rem 0; font-family:Syne,sans-serif;'>DataSante 232</h2>
        <p style='color:#607d8b; font-size:0.8rem;'>INF 232 EC2 — Analyse de donnees</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    menu = st.selectbox(
        "Navigation",
        [
            "Accueil",
            "Collecte des donnees",
            "Analyse descriptive",
            "Visualisations",
            "Gestion des donnees",
        ]
    )

    st.markdown("---")
    nb = len(st.session_state.data)
    st.markdown(f"""
    <div class='metric-card'>
        <h2>{nb}</h2>
        <p>Enregistrements collectes</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#90a4ae; text-align:center;'>
        <b>INF 232 EC2</b> · Mercredi 7h-10h<br>
        Secteur : Sante Communautaire
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE : ACCUEIL
# ─────────────────────────────────────────────
if menu == "Accueil":
    st.markdown("""
    <div class='main-header'>
        <h1>DataSante 232</h1>
        <p>Application de Collecte et Analyse Descriptive des Donnees de Sante Communautaire</p>
        <p style='font-size:0.8rem; color:#78909c;'>INF 232 EC2 — Travaux Pratiques · Prof. Francis ROLLIN</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    df = st.session_state.data

    with col1:
        st.markdown(f"""<div class='metric-card'><h2>{len(df)}</h2><p>Patients enregistres</p></div>""", unsafe_allow_html=True)
    with col2:
        moy = round(df["age"].mean(), 1) if not df.empty and "age" in df.columns else "—"
        st.markdown(f"""<div class='metric-card'><h2>{moy}</h2><p>Age moyen (ans)</p></div>""", unsafe_allow_html=True)
    with col3:
        pct_f = round((df["sexe"] == "Feminin").mean() * 100, 1) if not df.empty and "sexe" in df.columns else "—"
        st.markdown(f"""<div class='metric-card'><h2>{pct_f}{'%' if pct_f != '—' else ''}</h2><p>Femmes</p></div>""", unsafe_allow_html=True)
    with col4:
        moy_imc = round(df["imc"].mean(), 1) if not df.empty and "imc" in df.columns else "—"
        st.markdown(f"""<div class='metric-card'><h2>{moy_imc}</h2><p>IMC moyen</p></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class='info-box'>
    <b>Objectif du TP INF 232 EC2</b> : Developper une application robuste de collecte et d'analyse descriptive de donnees.
    Cette application couvre les themes : Regression lineaire, Reduction de dimensionnalite, Classification supervisee et non-supervisee.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### Fonctionnalites")
        st.markdown("""
        - Formulaire de saisie structure (donnees de sante)
        - Validation et stockage persistant (CSV)
        - Statistiques descriptives automatiques
        - Visualisations : histogrammes, boxplots, nuages de points, camembert
        - Export des donnees en CSV et Excel
        - Import de fichiers CSV existants
        """)
    with col_b:
        st.markdown("### Secteur : Sante Communautaire")
        st.markdown("""
        Les donnees collectees concernent :
        - Profil demographique des patients
        - Indicateurs biometriques (poids, taille, IMC)
        - Parametres cardiovasculaires
        - Habitudes de vie (activite physique, tabagisme)
        - Antecedents medicaux familiaux
        """)

# ─────────────────────────────────────────────
#  PAGE : COLLECTE DES DONNEES
# ─────────────────────────────────────────────
elif menu == "Collecte des donnees":
    st.markdown("<div class='section-title'>Formulaire de Collecte — Fiche Patient</div>", unsafe_allow_html=True)

    with st.form("formulaire_patient", clear_on_submit=True):

        st.markdown("#### Informations demographiques")
        c1, c2, c3 = st.columns(3)
        with c1:
            nom = st.text_input("Nom complet *", placeholder="Ex: Jean Dupont")
            date_naissance = st.date_input(
                "Date de naissance *",
                min_value=datetime.date(1920, 1, 1),
                max_value=datetime.date.today()
            )
        with c2:
            sexe = st.selectbox("Sexe *", ["Masculin", "Feminin"])
            region = st.selectbox("Region", [
                "Libreville", "Port-Gentil", "Franceville", "Oyem",
                "Moanda", "Lambarene", "Tchibanga", "Koulamoutou", "Autre"
            ])
        with c3:
            niveau_etude = st.selectbox("Niveau d'etudes", [
                "Aucun", "Primaire", "Secondaire", "Bac", "Licence", "Master", "Doctorat"
            ])
            profession = st.selectbox("Profession", [
                "Etudiant", "Salarie", "Commercant", "Agriculteur",
                "Fonctionnaire", "Retraite", "Sans emploi", "Autre"
            ])

        st.markdown("---")
        st.markdown("#### Indicateurs Biometriques")
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            poids = st.number_input("Poids (kg) *", min_value=10.0, max_value=300.0, step=0.5)
        with b2:
            taille = st.number_input("Taille (cm) *", min_value=50.0, max_value=250.0, step=0.5)
        with b3:
            tension_sys = st.number_input("Tension systolique (mmHg)", min_value=60, max_value=250, value=120)
        with b4:
            tension_dia = st.number_input("Tension diastolique (mmHg)", min_value=40, max_value=150, value=80)

        st.markdown("---")
        st.markdown("#### Habitudes de Vie et Antecedents")
        h1, h2, h3 = st.columns(3)
        with h1:
            tabac = st.selectbox("Tabagisme", ["Non-fumeur", "Ex-fumeur", "Fumeur occasionnel", "Fumeur regulier"])
            alcool = st.selectbox("Consommation d'alcool", ["Jamais", "Occasionnel", "Modere", "Frequent"])
        with h2:
            activite = st.selectbox("Activite physique", ["Sedentaire", "Legere", "Moderee", "Intense"])
            diabete = st.selectbox("Diabete", ["Non", "Type 1", "Type 2", "Prediabete"])
        with h3:
            hypertension = st.selectbox("Hypertension", ["Non", "Oui", "Sous traitement"])
            antecedents = st.multiselect("Antecedents familiaux", [
                "Cardiopathie", "Cancer", "Diabete", "Hypertension", "AVC", "Aucun"
            ])

        st.markdown("---")
        commentaire = st.text_area("Observations medicales (optionnel)", height=80)

        submitted = st.form_submit_button("Enregistrer le patient", use_container_width=True)

        if submitted:
            if not nom.strip():
                st.error("Le nom est obligatoire.")
            elif poids <= 0 or taille <= 0:
                st.error("Le poids et la taille doivent etre positifs.")
            else:
                age = (datetime.date.today() - date_naissance).days // 365
                imc = round(poids / ((taille / 100) ** 2), 2)
                if imc < 18.5:
                    cat_imc = "Insuffisance ponderale"
                elif imc < 25:
                    cat_imc = "Poids normal"
                elif imc < 30:
                    cat_imc = "Surpoids"
                else:
                    cat_imc = "Obesite"

                nouvelle_ligne = {
                    "nom": nom,
                    "date_naissance": str(date_naissance),
                    "age": age,
                    "sexe": sexe,
                    "region": region,
                    "niveau_etude": niveau_etude,
                    "profession": profession,
                    "poids": poids,
                    "taille": taille,
                    "imc": imc,
                    "categorie_imc": cat_imc,
                    "tension_systolique": tension_sys,
                    "tension_diastolique": tension_dia,
                    "tabac": tabac,
                    "alcool": alcool,
                    "activite_physique": activite,
                    "diabete": diabete,
                    "hypertension": hypertension,
                    "antecedents_familiaux": ", ".join(antecedents) if antecedents else "Aucun",
                    "commentaire": commentaire,
                    "date_collecte": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
                }

                nouveau_df = pd.DataFrame([nouvelle_ligne])
                st.session_state.data = pd.concat(
                    [st.session_state.data, nouveau_df], ignore_index=True
                )
                sauvegarder_donnees(st.session_state.data)

                st.markdown(f"""
                <div class='success-box'>
                    Patient <b>{nom}</b> enregistre avec succes.
                    Age calcule : <b>{age} ans</b> | IMC : <b>{imc}</b> ({cat_imc})
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE : ANALYSE DESCRIPTIVE
# ─────────────────────────────────────────────
elif menu == "Analyse descriptive":
    st.markdown("<div class='section-title'>Statistiques Descriptives</div>", unsafe_allow_html=True)

    df = st.session_state.data

    if df.empty:
        st.markdown("<div class='info-box'>Aucune donnee disponible. Commencez par collecter des donnees.</div>", unsafe_allow_html=True)
    else:
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        tab1, tab2, tab3 = st.tabs(["Variables numeriques", "Variables categorielles", "Donnees brutes"])

        with tab1:
            if num_cols:
                stats = df[num_cols].describe().T.round(2)
                stats["variance"] = df[num_cols].var().round(2)
                stats["skewness"] = df[num_cols].skew().round(2)
                stats["kurtosis"] = df[num_cols].kurt().round(2)
                st.dataframe(stats, use_container_width=True)

                st.markdown("#### Matrice de correlation")
                if len(num_cols) >= 2:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    corr = df[num_cols].corr()
                    mask = np.triu(np.ones_like(corr, dtype=bool))
                    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
                                cmap="coolwarm", ax=ax, linewidths=0.5,
                                cbar_kws={"shrink": 0.8})
                    ax.set_title("Correlation entre variables numeriques", fontsize=13, fontweight="bold")
                    st.pyplot(fig)
                    plt.close()
            else:
                st.info("Pas de variables numeriques disponibles.")

        with tab2:
            useful_cats = [c for c in cat_cols if c not in ["nom", "commentaire", "date_naissance", "date_collecte"]]
            if useful_cats:
                col_sel = st.selectbox("Choisir une variable", useful_cats)
                vc = df[col_sel].value_counts().reset_index()
                vc.columns = [col_sel, "Effectif"]
                vc["Frequence (%)"] = (vc["Effectif"] / len(df) * 100).round(1)
                vc["Freq. cumulee (%)"] = vc["Frequence (%)"].cumsum().round(1)
                st.dataframe(vc, use_container_width=True)

                fig2, ax2 = plt.subplots(figsize=(8, 4))
                colors = sns.color_palette("Set2", len(vc))
                bars = ax2.bar(vc[col_sel], vc["Effectif"], color=colors, edgecolor="white")
                for bar, val in zip(bars, vc["Effectif"]):
                    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                             str(val), ha="center", va="bottom", fontsize=10, fontweight="bold")
                ax2.set_title(f"Distribution de : {col_sel}", fontsize=13, fontweight="bold")
                ax2.set_xlabel(col_sel)
                ax2.set_ylabel("Effectif")
                plt.xticks(rotation=30, ha="right")
                st.pyplot(fig2)
                plt.close()
            else:
                st.info("Pas de variables categorielles disponibles.")

        with tab3:
            st.dataframe(df, use_container_width=True, height=400)
            st.caption(f"Total : {len(df)} enregistrements · {len(df.columns)} variables")

# ─────────────────────────────────────────────
#  PAGE : VISUALISATIONS
# ─────────────────────────────────────────────
elif menu == "Visualisations":
    st.markdown("<div class='section-title'>Visualisations Graphiques</div>", unsafe_allow_html=True)

    df = st.session_state.data

    if df.empty:
        st.markdown("<div class='info-box'>Aucune donnee disponible.</div>", unsafe_allow_html=True)
    else:
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = [c for c in df.select_dtypes(include="object").columns
                    if c not in ["nom", "commentaire", "date_naissance", "date_collecte"]]

        type_viz = st.selectbox("Type de visualisation", [
            "Histogramme",
            "Boite a moustaches (Boxplot)",
            "Nuage de points (Scatter)",
            "Diagramme circulaire (Camembert)",
            "Comparaison par groupe",
        ])

        if type_viz == "Histogramme":
            var = st.selectbox("Variable numerique", num_cols)
            bins = st.slider("Nombre de classes", 5, 50, 15)
            fig, ax = plt.subplots(figsize=(9, 5))
            ax.hist(df[var].dropna(), bins=bins, color="#1565c0", edgecolor="white", alpha=0.85)
            ax.axvline(df[var].mean(), color="#f44336", linestyle="--", linewidth=2, label=f"Moyenne : {df[var].mean():.2f}")
            ax.axvline(df[var].median(), color="#43a047", linestyle="--", linewidth=2, label=f"Mediane : {df[var].median():.2f}")
            ax.legend(fontsize=10)
            ax.set_title(f"Distribution de : {var}", fontsize=14, fontweight="bold")
            ax.set_xlabel(var)
            ax.set_ylabel("Frequence")
            st.pyplot(fig)
            plt.close()

        elif type_viz == "Boite a moustaches (Boxplot)":
            var = st.selectbox("Variable numerique", num_cols)
            groupe = st.selectbox("Grouper par (optionnel)", ["Aucun"] + cat_cols)
            fig, ax = plt.subplots(figsize=(9, 5))
            if groupe == "Aucun":
                ax.boxplot(df[var].dropna(), patch_artist=True,
                           boxprops=dict(facecolor="#90caf9", color="#1565c0"),
                           medianprops=dict(color="#f44336", linewidth=2))
                ax.set_xticks([1])
                ax.set_xticklabels([var])
            else:
                groups = [df[df[groupe] == g][var].dropna().values for g in df[groupe].unique()]
                labels = list(df[groupe].unique())
                bplot = ax.boxplot(groups, patch_artist=True, labels=labels)
                colors = sns.color_palette("Set2", len(labels))
                for patch, c in zip(bplot["boxes"], colors):
                    patch.set_facecolor(c)
            ax.set_title(
                f"Boxplot de {var}" + (f" par {groupe}" if groupe != "Aucun" else ""),
                fontsize=13, fontweight="bold"
            )
            plt.xticks(rotation=30, ha="right")
            st.pyplot(fig)
            plt.close()

        elif type_viz == "Nuage de points (Scatter)":
            if len(num_cols) < 2:
                st.warning("Il faut au moins 2 variables numeriques.")
            else:
                c1, c2 = st.columns(2)
                with c1:
                    vx = st.selectbox("Variable X", num_cols, index=0)
                with c2:
                    vy = st.selectbox("Variable Y", num_cols, index=min(1, len(num_cols) - 1))
                couleur = st.selectbox("Couleur par groupe (optionnel)", ["Aucun"] + cat_cols)

                fig, ax = plt.subplots(figsize=(9, 5))
                if couleur == "Aucun":
                    ax.scatter(df[vx], df[vy], color="#1565c0", alpha=0.7, edgecolors="white")
                else:
                    palette = sns.color_palette("Set1", df[couleur].nunique())
                    for i, g in enumerate(df[couleur].unique()):
                        sub = df[df[couleur] == g]
                        ax.scatter(sub[vx], sub[vy], label=g, alpha=0.7, color=palette[i], edgecolors="white")
                    ax.legend()

                valid = df[[vx, vy]].dropna()
                if len(valid) >= 2:
                    m, b = np.polyfit(valid[vx], valid[vy], 1)
                    xline = np.linspace(valid[vx].min(), valid[vx].max(), 100)
                    ax.plot(xline, m * xline + b, color="#f44336", linewidth=2, linestyle="--", label="Droite de regression")
                    r = valid[[vx, vy]].corr().iloc[0, 1]
                    ax.set_title(f"{vx} vs {vy}  (r = {r:.3f})", fontsize=13, fontweight="bold")
                ax.set_xlabel(vx)
                ax.set_ylabel(vy)
                ax.legend()
                st.pyplot(fig)
                plt.close()

        elif type_viz == "Diagramme circulaire (Camembert)":
            if not cat_cols:
                st.warning("Pas de variable categorielle disponible.")
            else:
                var = st.selectbox("Variable categorielle", cat_cols)
                vc = df[var].value_counts()
                fig, ax = plt.subplots(figsize=(7, 7))
                colors = sns.color_palette("Set2", len(vc))
                wedges, texts, autotexts = ax.pie(
                    vc.values, labels=vc.index, autopct="%1.1f%%",
                    colors=colors, startangle=90,
                    wedgeprops=dict(edgecolor="white", linewidth=2)
                )
                for at in autotexts:
                    at.set_fontsize(10)
                    at.set_fontweight("bold")
                ax.set_title(f"Repartition de : {var}", fontsize=13, fontweight="bold")
                st.pyplot(fig)
                plt.close()

        elif type_viz == "Comparaison par groupe":
            if not cat_cols or not num_cols:
                st.warning("Il faut au moins une variable categorielle et une variable numerique.")
            else:
                c1, c2 = st.columns(2)
                with c1:
                    cat_var = st.selectbox("Variable groupe", cat_cols)
                with c2:
                    num_var = st.selectbox("Variable numerique", num_cols)

                grouped = df.groupby(cat_var)[num_var].agg(["mean", "median", "std"]).round(2).reset_index()
                grouped.columns = [cat_var, "Moyenne", "Mediane", "Ecart-type"]
                st.dataframe(grouped, use_container_width=True)

                fig, ax = plt.subplots(figsize=(9, 5))
                palette = sns.color_palette("Set2", len(grouped))
                bars = ax.bar(grouped[cat_var], grouped["Moyenne"], color=palette, edgecolor="white")
                for bar, val in zip(bars, grouped["Moyenne"]):
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                            f"{val:.1f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
                ax.set_title(f"Moyenne de {num_var} par {cat_var}", fontsize=13, fontweight="bold")
                ax.set_xlabel(cat_var)
                ax.set_ylabel(f"Moyenne de {num_var}")
                plt.xticks(rotation=30, ha="right")
                st.pyplot(fig)
                plt.close()

# ─────────────────────────────────────────────
#  PAGE : GESTION DES DONNEES
# ─────────────────────────────────────────────
elif menu == "Gestion des donnees":
    st.markdown("<div class='section-title'>Import / Export des Donnees</div>", unsafe_allow_html=True)

    df = st.session_state.data
    tab1, tab2, tab3 = st.tabs(["Import", "Export", "Nettoyage"])

    with tab1:
        st.markdown("#### Importer un fichier CSV")
        uploaded = st.file_uploader("Choisir un fichier CSV", type=["csv"])
        if uploaded:
            try:
                imported = pd.read_csv(uploaded)
                st.success(f"Fichier charge : {len(imported)} lignes, {len(imported.columns)} colonnes")
                st.dataframe(imported.head(10), use_container_width=True)
                if st.button("Fusionner avec les donnees actuelles"):
                    st.session_state.data = pd.concat([df, imported], ignore_index=True)
                    sauvegarder_donnees(st.session_state.data)
                    st.success("Donnees fusionnees et sauvegardees.")
                if st.button("Remplacer les donnees actuelles"):
                    st.session_state.data = imported
                    sauvegarder_donnees(st.session_state.data)
                    st.success("Donnees remplacees.")
            except Exception as e:
                st.error(f"Erreur de lecture : {e}")

    with tab2:
        if df.empty:
            st.info("Aucune donnee a exporter.")
        else:
            st.markdown(f"**{len(df)} enregistrements** disponibles a l'export.")

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Telecharger CSV",
                data=csv,
                file_name=f"datasante_232_{datetime.date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )

            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Donnees", index=False)
                num_cols = df.select_dtypes(include=np.number).columns.tolist()
                if num_cols:
                    df[num_cols].describe().round(2).to_excel(writer, sheet_name="Statistiques")
            buffer.seek(0)
            st.download_button(
                "Telecharger Excel",
                data=buffer,
                file_name=f"datasante_232_{datetime.date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    with tab3:
        if df.empty:
            st.info("Aucune donnee disponible.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Valeurs manquantes")
                manq = df.isnull().sum()
                manq = manq[manq > 0]
                if manq.empty:
                    st.success("Aucune valeur manquante detectee.")
                else:
                    st.dataframe(manq.rename("Nb manquants"), use_container_width=True)
                    if st.button("Supprimer les lignes incompletes"):
                        avant = len(df)
                        st.session_state.data = df.dropna()
                        sauvegarder_donnees(st.session_state.data)
                        st.success(f"{avant - len(st.session_state.data)} ligne(s) supprimee(s).")
            with col2:
                st.markdown("#### Doublons")
                dupl = df.duplicated().sum()
                if dupl == 0:
                    st.success("Aucun doublon detecte.")
                else:
                    st.warning(f"{dupl} doublon(s) detecte(s).")
                    if st.button("Supprimer les doublons"):
                        st.session_state.data = df.drop_duplicates()
                        sauvegarder_donnees(st.session_state.data)
                        st.success("Doublons supprimes.")

            st.markdown("---")
            st.markdown("#### Reinitialisation des donnees")
            if st.button("Supprimer toutes les donnees", type="secondary"):
                confirm = st.checkbox("Je confirme la suppression definitive de toutes les donnees")
                if confirm:
                    st.session_state.data = pd.DataFrame()
                    if os.path.exists(DATA_FILE):
                        os.remove(DATA_FILE)
                    st.error("Toutes les donnees ont ete supprimees.")
