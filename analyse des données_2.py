#!/usr/bin/env python
# coding: utf-8

# In[89]:


import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go


# In[45]:


data = pd.read_csv('C:/Users/HP/Documents/challenge sécurité/challenge-2023/données/log_fw_3.csv',header=None ,delimiter=';',names=['Date','IP source', 'Ip destination','protocole','port source','port à destination','G','action','I','J','K'],index_col=False)
data


# In[28]:


data.shape[1]


# In[83]:


#top 5 des adresses IP les plus actives 
def plot_top_ip_addresses(dataframe, Ip_column_name, n=5):
    # Compter le nombre d'occurrences de chaque adresse IP
    ip_counts = dataframe[Ip_column_name].value_counts()

    # Sélectionner les n adresses IP les plus actives
    top_ips = ip_counts[:n]

    # Créer un dataframe avec les données pour le graphique
    data = {'Adresse IP': top_ips.index, 'Nombre d\'occurrences': top_ips.values}
    df = pd.DataFrame(data)

    # Tracer le diagramme à barres avec Plotly
    fig = px.bar(df, x='Adresse IP', y='Nombre d\'occurrences', color='Adresse IP')
    fig.update_layout(title=f'Top {n} des adresses IP les plus actives', xaxis_title='Adresse IP', yaxis_title='Nombre d\'occurrences')
    fig.show()


# In[85]:


plot_top_ip_addresses( data,'IP source', n=5)


# In[101]:


#TOP 10 des ports inférieurs à 1024 avec un accès autorisé,
def plot_top_allowed_ports(dataframe):
    # Filtrer les données pour n'avoir que les accès autorisés et les ports inférieurs à 1024
    filtered_data = dataframe[(dataframe['action'] == 'PERMIT') & (dataframe['port à destination'] < 1024)]

    # Compter le nombre d'occurrences pour chaque port
    port_counts = filtered_data['port à destination'].value_counts().sort_values(ascending=False).head(10)

    # Tracer le graphique des TOP 10 des ports autorisés
    fig = go.Figure([go.Bar(x=port_counts.index.astype(str), y=port_counts.values, text=['Port ' + str(p) for p in port_counts.index], textposition='auto')])
    fig.update_layout(title='TOP 10 des ports inférieurs à 1024 avec un accès autorisé', xaxis_title='Port', yaxis_title='Nombre d\'accès autorisés')
    fig.show()


# In[102]:


plot_top_allowed_ports(data)

# Analyse temporelle
# In[57]:


data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d %H:%M:%S")


# In[81]:


def plot_tcp_flows(dataframe):
    # Filtrer les données pour n'avoir que les flux TCP autorisés et rejetés
    filtered_data = dataframe[dataframe['protocole'] == 'TCP']
    permitted_flows = filtered_data[filtered_data['action'] == 'PERMIT']
    denied_flows = filtered_data[filtered_data['action'] == 'DENY']

    # Compter le nombre de flux autorisés et rejetés par heure
    permitted_counts = permitted_flows.groupby(pd.Grouper(key='Date', freq='H')).size()
    denied_counts = denied_flows.groupby(pd.Grouper(key='Date', freq='H')).size()

    # Tracer le graphique des flux TCP autorisés et rejetés
    fig = px.line(title='Flux TCP autorisés et rejetés par heure')
    fig.add_scatter(x=permitted_counts.index, y=permitted_counts.values, mode='lines', name='Flux autorisés')
    fig.add_scatter(x=denied_counts.index, y=denied_counts.values, mode='lines', name='Flux rejetés')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Nombre de flux')
    fig.show()


# In[82]:


plot_tcp_flows(data)


# In[79]:


def plot_event_hour(dataframe):
    hour_of_event = pd.to_datetime(dataframe['Date']).dt.hour
    eventdata = pd.DataFrame({'datetime': dataframe['Date'], 'eventhour': hour_of_event})
    eventdata['Horaire'] = (eventdata['eventhour'] >= 7) & (eventdata['eventhour'] <= 18)
    eventdata['Horaire'] = eventdata['Horaire'].apply(lambda x: 'Horaires ouvrés' if x else 'Horaires non ouvrés')

    # Créer le graphique
    fig = px.histogram(eventdata, x='eventhour', color='Horaire', nbins=24,
                        category_orders={'Horaire': ['Horaires ouvrés', 'Horaires non ouvrés']},
                        labels={'eventhour': 'Heure de la journée', 'count': 'Nombre d\'événements'})
    fig.update_layout(title='Distribution des événements par heure')
    fig.show()


# In[80]:


plot_event_hour(data)

