import streamlit as st
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from IPsrc_functions import *

os.chdir(r'C:\Documents\GitHub\Challenge_OPSIE-SISE')

def main():
    st.header("Challenge SISE - OPSIE - 2023")
   
if __name__ == '__main__':
    main()

df = pd.read_csv('log_fw_3.csv', sep=';',header=None, encoding='latin-1')
df=prepare_log_data(df)
st.subheader('Données brutes')
st.write(df)
st.text('La base sélectionnée contient : ' + str(df.shape[0]) + " lignes")


st.session_state.df = df