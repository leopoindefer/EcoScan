import pandas as pd
import streamlit as st
import numpy as np
import re
import json
import plotly.express as px

st.title('EcoScan')

data = pd.read_csv('data/data.csv', sep=',')
col_a_supp = ["Label","Région","Pdf","Logo"]
data = data.drop(col_a_supp, axis=1)
data[['Note Globale','Limitation Des Impacts Négatifs','Partage Du Pouvoir Et De La Valeur','Stratégie à Impact Positif']] = data[['Note Globale','Limitation Des Impacts Négatifs','Partage Du Pouvoir Et De La Valeur','Stratégie à Impact Positif']].apply(pd.to_numeric)
col = data.columns[1:]
data[col] = data[col].apply(pd.to_numeric, errors='coerce').astype(float)
data = data.fillna(0)
data[col] = data[col].mask(data[col] > 100, 100)
data = data.T
data.columns = data.iloc[0]
data = data.drop(data.index[0])
data["Orga"] = data.index
data_pref = data.copy()
data_pref = data.iloc[-19:]
data = data.iloc[:4]

marques = data.columns.unique()
tab1,tab2 = st.tabs(["Scanner un produit","Plus de détail"])

with st.sidebar:
    st.title("Mes préférences")
    st.header("Limitation des impacts négatifs")
    impact_social = st.radio("Impact social",("Inclusion des travailleurs éloignés de l'emploi","Soutien de publics fragiles","Egalité Femmes-Hommes","Intégration des jeunes et seinors"))
    impact_ecologique = st.radio("Impact écologique",("Mesure de l'empreinte carbone","Réduction de l'empreinte carbone","Biodiversité et utilisation des ressources naturelles","Economie locale et circulaire"))
    st.header("Partage de la valeur et du pouvoir")
    partage_du_pouvoir = st.radio("Partage du pouvoir",("Partie prenantes dans la gouvernance","Place des salariés dans la décision","Progression des salariés","Stabilité au travail"))
    partage_de_la_valeur = st.radio("Partage de la valeur",("Partage de la valeur entre les parties prenantes","Ecarts de rémunération","Placement financiers responsables","Mécénat"))
    st.header("Stratégie à impact positif")
    engagement_dev_durable = st.radio("Engagement pour les objectifs de développement durable",("Impact du coeur d'activité","Labels et certifications","Achats responsables"))
with tab1:
    st.header("Scanner une marque")
    marque = st.selectbox("Choisir une marque",marques)
    try:
        data_pref = data_pref.loc[:,[marque]]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label=impact_social, value=data_pref.iloc[0])
        with col2:
            st.metric(impact_ecologique, value=data_pref.iloc[1])
        with col3:
            st.metric(partage_du_pouvoir, value=data_pref.iloc[2])
        col12, col22 = st.columns(2)
        with col12:
            st.metric(partage_de_la_valeur, value=data_pref.iloc[3])
        with col22:
            st.metric(engagement_dev_durable, value=data_pref.iloc[4])
    except:
        st.error("Pas de donnée")
    fig = px.line_polar(data, r=marque, theta='Orga', line_close=True)
    fig.update_traces(fill='toself')

    st.plotly_chart(fig, use_container_width=True)
with tab2:
    st.header("Plus de détail")