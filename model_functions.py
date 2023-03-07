import pandas as pd
import plotly.express as px



def to_datetime(x):
    return pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S.%f')

def prepare_log_data(log_data):
    log_data.columns = ['timestamp', 'IPsrc', 'IPdst', 'proto', 'portsrc', 'portdst', 'rule','action','7', '8','9']
    log_data.timestamp = to_datetime(log_data.timestamp)
    log_data.portdst = log_data.portdst.astype('object')
    return log_data

# create function of the above
def get_IPsrc_stats(data):
    IPsrc_deny = data[data.action == 'DENY'].groupby('IPsrc')['IPdst'].count().sort_values(ascending=False)
    IPsrc_deny = pd.DataFrame([IPsrc_deny.index,IPsrc_deny]).transpose()
    IPsrc_deny.columns = ['IPsrc', 'deny_count']
    mean_timestamp_byIP = data.groupby('IPsrc').timestamp.mean().reset_index(name='mean_timestamp').sort_values(by='mean_timestamp', ascending=False)
    IPsrc_counts = data.groupby('IPsrc').size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    return IPsrc_deny, mean_timestamp_byIP, IPsrc_counts

# create function to create df_supervised with IPsrc_deny, mean_timestamp_byIP, IPsrc_counts

def create_unsupervised_df(data):
    IPsrc_deny, mean_timestamp_byIP, IPsrc_counts = get_IPsrc_stats(data)
    ratio = pd.merge(IPsrc_counts, IPsrc_deny, on='IPsrc')
    ratio['ratio_deny_total'] = ratio['deny_count'] / ratio['counts']
    df_supervised = pd.merge(IPsrc_counts, mean_timestamp_byIP, on='IPsrc')
    df_supervised = pd.merge(df_supervised, ratio[['IPsrc','ratio_deny_total']], on='IPsrc')


    df_supervised['hour'] = df_supervised.mean_timestamp.dt.hour
    return df_supervised

def pie_pred(data):
    res_pred = data.groupby('prediction_class').size().reset_index(name='counts')
    # plot pie chart
    fig = px.pie(res_pred, values="counts", names="prediction_class", color="prediction_class", title="Prediction distribution")
    return fig

    

# données opsie 


def prepare_log_data_opsie(log_data):
    log_data.columns = ['timestamp', 'IPsrc', 'IPdst', 'portdst', 'proto', 'action', 'rule']
    log_data.timestamp = to_datetime(log_data.timestamp)
    log_data.portdst = log_data.portdst.astype('object')
    return log_data

# create function of the above
def get_IPsrc_stats_opsie(data):
    IPsrc_deny = data[data.action == 'Deny'].groupby('IPsrc')['IPdst'].count().sort_values(ascending=False)
    IPsrc_deny = pd.DataFrame([IPsrc_deny.index,IPsrc_deny]).transpose()
    IPsrc_deny.columns = ['IPsrc', 'deny_count']
    mean_timestamp_byIP = data.groupby('IPsrc').timestamp.mean().reset_index(name='mean_timestamp').sort_values(by='mean_timestamp', ascending=False)
    IPsrc_counts = data.groupby('IPsrc').size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    return IPsrc_deny, mean_timestamp_byIP, IPsrc_counts

# create function to create df_supervised with IPsrc_deny, mean_timestamp_byIP, IPsrc_counts

def create_unsupervised_df_opsie(data):
    IPsrc_deny, mean_timestamp_byIP, IPsrc_counts = get_IPsrc_stats_opsie(data)
    ratio = pd.merge(IPsrc_counts, IPsrc_deny, on='IPsrc')
    ratio['ratio_deny_total'] = ratio['deny_count'] / ratio['counts']
    
    df_supervised = pd.merge(IPsrc_counts, mean_timestamp_byIP, on='IPsrc')
    df_supervised = pd.merge(df_supervised, ratio[['IPsrc','ratio_deny_total']], on='IPsrc')


    df_supervised['hour'] = df_supervised.mean_timestamp.dt.hour
    return df_supervised

   

