import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from IPsrc_functions import prepare_log_data, create_merge_IPsrc, ratio_class

def add_port_type(dataframe):
    prepare_log_data(dataframe)
    dataframe['port_type'] = dataframe['portdst'].apply(lambda x: 'wk' if x < 1024 else ('reg' if x >= 1024 and x <= 49151 else 'priv'))
    return dataframe

def clas_proto(dataframe):
    add_port_type(dataframe)
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
    fig.show()



def plot_action_by_port_type(dataframe):
    tcp, udp = clas_proto(dataframe)
    tcp_deny, tcp_permit = class_acc_pro(tcp)
    udp_deny, udp_permit = class_acc_pro(udp)
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=tcp_permit['port_type'], name='TCP PERMIT'))
    fig.add_trace(go.Histogram(x=udp_permit['port_type'], name='UDP PERMIT'))
    fig.add_trace(go.Histogram(x=tcp_deny['port type'], name='TCP DENIED'))
    fig.add_trace(go.Histogram(x=udp_deny['port type'], name='UDP DENIED'))
    fig.update_layout(title='Action by port type', xaxis_title='Port', yaxis_title='Nombre d\'accès')
    fig.show()

''''''