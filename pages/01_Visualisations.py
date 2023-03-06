import streamlit as st
from 01_Visualisations import *

st.title('Visualisation des données')

Diagramme = st.sidebar.radio(
        "Choix du graphique",
        ("Adresses IP actives", "Ports inférieurs à 1024","Evènements par heure","Actions flux TCP"))

#Affichage des graphiques
if Diagramme == "Adresses IP actives":
    st.subheader("Adresses IP actives")
    st.bar_chart(plot_top_ip_addresses(st.session_state['df'], 'src_ip', n=5))
