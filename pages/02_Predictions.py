import streamlit as st
import pickle

st.title('Prédictions du modèle')

# load the model from disk and use cashing to speed up the loading
@st.cache(allow_output_mutation=True)
def load_model():
    loaded_model = pickle.load(open('model/IsolationForest_model.pkl', 'rb'))
    return loaded_model
with st.spinner('Loading Model Into Memory...'):
    model = load_model()



