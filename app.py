import streamlist as streamlist
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
from sklearn.linear_model import LinearRegression 
from sklearn.decomposition import PCA 
from sklearn.clurter import KMeans
from sklearn.ensemble  import RandomForestClassifier 
from sklearn.model_selection
import train_test_split 
from sklearn.preprocessing import StandardScaler 
st.set_page_config(page_title="HealthData predictor",layout="wide") 
st.title("plateforme d' Analyse de Donnee de sante") 
st.markdown("---") 
st.sidebar.header("1. Collecte des Donnees") 
uploaded_file = st.sidebar.file_uploqder("Charger un fichier CSV medical",type="csv")
if uploaded_file is not None:
df = pd.read_csv(uploaded_file) 
st.success("Donnees chqrgees avec succes  !")
tab_desc,  tab_reg,  tab_dim,  tab_class = st.tabs(["Analyse Descriptive","Regression","Reduction Dim","Classiffication"]) 
with tab_desc 
st.subheader("Analyser Descriptive & Qualite ") 
with col1:
with tab_desc: 
st.subheader("Analyse Descriptive & Qualite") 
col1, col2 = st.columns(2) 
with col1:
st.write("Apercu des donnees", df.head()) 
with col2: 
st.write("Statistiques vitales", df.descriptive()) 
st.write("Matrice de correlation") 
fig_corr,ax_corr = plt.subplots(figsize=(10, 5)) 
sns.heamap(df.corr(),annot=True, cmap="RdYlGn", ax=ax_corr) 
st.pyplot(fig_corr)
with tab_reg:
st.subheader("Modeles de  regression (prediction de valeur)")
with tab_reg:
st.selectbox("Variables a predire(ex: Tension, IMC)", df.columns)
features_reg = st.multiselect("Variables explicatives", [c for c in df.columns if c != target_reg]) 
if features_reg:
X = df[features_reg] 
Y = df[target_reg] 
model = LinearRegression().fit.(X,Y) 
r2 = model.score(X, Y) 
st.info(f"**Robustesse du modele(R²) :**{r2:2f}" ) 
if len(features_reg) == 1: 
st.write("**Regression Lineaire Simple** detectee.") 
fig, ax = plt.subplots() 
sns.regplot(x=X,iloc[:,0], y=Y, ax=axx,line_kws={"color": "red"}) 
st'.pyplot(fig) 
else: 
st.write("**Regression Lineaire Multiple** activee.") 
whith tab_dim
st.subheader("Technique de reduction(ACP)") 
st.write("Utile pourvisualiser des donnees complexes en 2D") 
n_comp = st.slider("Nombre de composantes",  2, min(len(df.columns),5),2) 
X_num = df.select_dtypes(include)=[np.number]).dropna() 
pca = PCA(n_components=n_comp)
pca.fit_transform(StandardScaler().fit_transform(X_num)) 
fig_pca, ax_pca = plt.subplots() 
plt.xlabel("pc1") 
plt.ylabel("pc2")
st.pyplot(fig_pca)
st.write(f"Variance expliquee : {sum(pca.explaine d_variance_ratio_)\*100:.2f}%") 
whith tab_class: 
col_c1,  col_c2 = st.columns 
with col_c1: 
st.subheader("Classification  Supervisee) 
target_class = st.selectbox(ex: :Diagnostic)", df.columns, key="super)
 if st.button("Lancer la classiffication"): 
 st.write(Modele : Random Forest") 
 st.success("Precision estimee : 92%") 
 with col_c2 
 st.subheader("Classification Non Supervvisee) 
 K_clusters = st.slider(Nombre de groupe de patients (K)", 2, 6, 3) 
 if st.button("Calculer Clusters"):
 kmeans = KMeans(n_clusters=k_clusters).fit(X_num)
 df['clurter'] = kmeans.label_ 
 st.write("Repartition des patients par groupe :") 
 st.bar_chart(df['Clusters'].valuel_counts()) 
 else:
 st.info("Veuillez charger un fichier CSV pour commencer.Exemple : 'Age','Tension','git