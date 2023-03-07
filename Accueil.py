import streamlit as st
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from IPsrc_functions import *
import mysql.connector

#os.chdir(r'C:\Documents\GitHub\Challenge_OPSIE-SISE')

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="logs"
)

#mycursor = mydb.cursor()
#req = "SELECT datetime, ipsrc, ipdst, proto, dstport, policyid, action FROM fw"
#df = pd.read_sql(req,mydb)
#df=prepare_log_sql(df)

df = pd.read_csv('log_fw_3.csv', sep=';',header=None, encoding='latin-1')
df=prepare_log_data(df)

def main():
    st.header("Challenge SISE - OPSIE - 2023")
   
if __name__ == '__main__':
    main()

#''' create a liste and a multiselect widget to select the data of the database between 2 dates and the dates have to be between 2023-02-12 and 2023-03-02'''
st.subheader('Sélection des données')
st.text('Sélectionnez les dates de début et de fin pour afficher les données de la base')
start_date = st.date_input('Date de début', value=df.timestamp.min())
end_date = st.date_input('Date de fin', value=df.timestamp.max())
df = df[(df.timestamp.dt.date >= start_date) & (df.timestamp.dt.date <= end_date)]



st.subheader('Données brutes')
st.write(df)
st.text('La base sélectionnée contient : ' + str(df.shape[0]) + " lignes")


st.session_state.df = df