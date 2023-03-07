import streamlit as st
from analyse_des_donnees_2 import *
from IPsrc_functions import *
from flux_proto import *

st.set_page_config(layout="wide")
st.title('Visualisations')

Diagramme = st.sidebar.radio(
        "Choix du graphique",
        ("Requêtes IP Source","Analyse temporelle","Flux par protocole"))

#Affichage des graphiques
if Diagramme == "Requêtes IP Source":
    Type = st.selectbox(f"Selectionner le type d'action à afficher :",["total", "deny","permit"])
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_pie(create_merge_IPsrc(st.session_state.df), Type))
    with col2:
        st.plotly_chart(plot_pie_ratio(ratio_count_df(create_merge_IPsrc(st.session_state.df)),'count'))    

    st.plotly_chart(plot_scatter(create_merge_IPsrc(st.session_state.df),'permit', 'deny'))
    st.plotly_chart(plot_top_ip_addresses(st.session_state.df,'IPsrc'))
    st.plotly_chart(plot_top_allowed_ports(st.session_state.df))

if Diagramme == "Analyse temporelle":
    st.plotly_chart(plot_tcp_flows(st.session_state.df,'timestamp'))
    st.plotly_chart(plot_event_hour(st.session_state.df,'timestamp'))
    #st.pyplot(circular_graph(st.session_state.df))

if Diagramme == "Flux par protocole":
    st.plotly_chart(plot_access_by_protocol(st.session_state.df))
    st.plotly_chart(plot_action_by_port_type(st.session_state.df))

    