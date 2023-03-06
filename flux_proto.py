import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from IPsrc_functions import prepare_log_data, create_merge_IPsrc, ratio_class

def clas_proto(dataframe):
    tcp = dataframe[(dataframe['protocole'] == 'TCP')]
    udp = dataframe[(dataframe['protocole'] == 'UDP')]
    return (tcp, udp)

def class_acc_pro(dataframe):
    deny = dataframe[(dataframe['action'] == 'DENY')]
    permit = dataframe[(dataframe['action'] == 'PERMIT')]
    return (deny, permit)   

''' function to plot the number of access by protocol '''
def plot_access_by_protocol(dataframe):
    tcp, udp = clas_proto(dataframe)
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=tcp['protocole'], name='TCP'))
    fig.add_trace(go.Histogram(x=udp['protocole'], name='UDP'))
    fig.update_layout(title='Nombre d\'accès par protocole', xaxis_title='Protocole', yaxis_title='Nombre d\'accès')
    return fig



def plot_action_by_port_type(dataframe):
    tcp, udp = clas_proto(dataframe)
    tcp_deny, tcp_permit = class_acc_pro(tcp)
    udp_deny, udp_permit = class_acc_pro(udp)
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=tcp_permit['port_type'], name='TCP PERMIT'))
    fig.add_trace(go.Histogram(x=udp_permit['port_type'], name='UDP PERMIT'))
    fig.add_trace(go.Histogram(x=tcp_deny['port_type'], name='TCP DENIED'))
    fig.add_trace(go.Histogram(x=udp_deny['port_type'], name='UDP DENIED'))
    fig.update_layout(title='Action by port type', xaxis_title='Port', yaxis_title='Nombre d\'accès')
    return fig

''' create a function that plots the lines of the nummber of accesses by date'''
def plot_access_by_date(dataframe):
    dataframe['date'] = dataframe['timestamp'].dt.date
    dataframe['hour'] = dataframe['timestamp'].dt.hour
    dataframe['day'] = dataframe['timestamp'].dt.day
    dataframe['month'] = dataframe['timestamp'].dt.month
    dataframe['year'] = dataframe['timestamp'].dt.year
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['date'], y=dataframe['date'], mode='lines', name='lines'))
    fig.update_layout(title='Nombre d\'accès par jour', xaxis_title='Jour', yaxis_title='Nombre d\'accès')
    return fig
