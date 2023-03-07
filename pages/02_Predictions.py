import streamlit as st
import pickle
import pandas as pd
from model_functions import *
import plotly.express as px

df = None
df_prep = None

st.title("Importez un fichier csv pour faire des prédictions")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file, sep=';',header=None, encoding='latin-1')
  st.write(df, df.shape)
  

st.title('Prédictions du modèle')

if df is not None:
    df_prep = create_unsupervised_df(prepare_log_data(df))
    X_unsupervised = df_prep[['counts', 'hour', 'ratio_deny_total']]
else : 
    st.write('_Aucun fichier n\'a été importé_' )

# load the model from disk and use cashing to speed up the loading
@st.cache(allow_output_mutation=True)
def load_model():
    loaded_model = pickle.load(open('pages/IsolationForest_model', 'rb'))
    return loaded_model
with st.spinner('Loading Model Into Memory...'):
    model = load_model()



# make predictions
with st.sidebar.form("Input"):
    if df is not None:
        btnResult = st.form_submit_button('Make Predictions', disabled=False)
    else :
        btnResult = st.form_submit_button('Make Predictions', disabled=True)
    

if btnResult:
    with st.spinner('Predicting...'):
        y_pred = model.predict(X_unsupervised)
        att = model.decision_function(X_unsupervised)
        df_prep['prediction_value'] = att
        df_prep['prediction_class'] = y_pred
        df_prep['prediction_class'] = df_prep['prediction_class'].apply(lambda x: 'Anomalie' if x == -1 else 'Normal')
        st.write(df_prep[['IPsrc', 'counts','prediction_class', 'prediction_value']])

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(pie_pred(df_prep), use_container_width=True)
        with col2:
            st.text('Top 10 des IPs les plus dangereuses prédites')
            st.write(df_prep[['IPsrc', 'counts', 'prediction_value']][df_prep.prediction_class == 'Anomalie'].sort_values(by='counts', ascending=False).head(10))
        



#st.title('Anomalies détectées')
#st.write(df_prep[df_prep.prediction_class == 'Anomalie'])
# sort 
   


