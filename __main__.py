import pandas as pd
import streamlit as st
import numpy as np
import re
import json
import plotly.express as px
import altair as alt

st.set_page_config(
    page_title="EcoMetrica",
    page_icon="🌿",
)

def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })

  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })

  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=24, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text
st.title('EcoMetrica')

st.markdown("----")

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
    st.header("Scanner une marque")

try:
    marque = st.selectbox("Scanner un logo",marques)
    st.camera_input()
    st.write("")
    data_pref = data_pref.loc[:,[marque]]
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div style='text-align: center;'>{impact_social}</div>",unsafe_allow_html=True)
        alt_is = make_donut(data_pref.loc[impact_social,marque], impact_social, 'blue')
        st.altair_chart(alt_is, use_container_width=True)
    with col2:
        st.markdown(f"<div style='text-align: center;'>{impact_ecologique}</div>",unsafe_allow_html=True)
        alt_ie = make_donut(data_pref.loc[impact_ecologique,marque], impact_ecologique, 'green')
        st.altair_chart(alt_ie, use_container_width=True)
    with col3:
        st.markdown(f"<div style='text-align: center;'>{partage_du_pouvoir}</div>",unsafe_allow_html=True)
        alt_pdp = make_donut(data_pref.loc[partage_du_pouvoir,marque], partage_du_pouvoir, 'red')
        st.altair_chart(alt_pdp, use_container_width=True)
    col12, col22 = st.columns(2)
    with col12:
        st.markdown(f"<div style='text-align: center;'>{partage_de_la_valeur}</div>",unsafe_allow_html=True)
        alt_pdv = make_donut(data_pref.loc[partage_de_la_valeur,marque], partage_de_la_valeur, 'orange')
        st.altair_chart(alt_pdv, use_container_width=True)
    with col22:
        st.markdown(f"<div style='text-align: center;'>{engagement_dev_durable}</div>",unsafe_allow_html=True)
        alt_edd = make_donut(data_pref.loc[engagement_dev_durable,marque], engagement_dev_durable, 'green')
        st.altair_chart(alt_edd, use_container_width=True)
except:
    st.error("Pas de donnée")

fig = px.line_polar(data, r=marque, theta='Orga', line_close=True)
fig.update_traces(fill='toself')
st.plotly_chart(fig, use_container_width=True)