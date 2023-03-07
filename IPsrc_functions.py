# Import packages 
import pandas as pd
import plotly.express as px

# Function list 

## Data preparation
def to_datetime(x):
    return pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S.%f')

def prepare_log_data(log_data):
    log_data.columns = ['timestamp', 'IPsrc', 'IPdst', 'protocole', 'portsrc', 'portdst', 'rule','action','7', '8','9']
    #log_data.timestamp = to_datetime(log_data.timestamp)
    log_data.timestamp = pd.to_datetime(log_data.timestamp, format="%Y-%m-%d %H:%M:%S")
    log_data.portdst = log_data.portdst.astype('object')
    log_data['port_type'] = log_data['portdst'].apply(lambda x: 'wk' if x < 1024 else ('reg' if x >= 1024 and x <= 49151 else 'priv'))
    return log_data

def prepare_log_sql(log_data):
    log_data.columns = ['timestamp', 'IPsrc', 'IPdst', 'protocole', 'portdst', 'rule','action']
    #log_data.timestamp = to_datetime(log_data.timestamp)
    log_data.timestamp = pd.to_datetime(log_data.timestamp, format="%Y-%m-%d %H:%M:%S")
    log_data.portdst = log_data.portdst.astype('object')
    
    #log_data['port_type'] = log_data['portdst'].apply(lambda x: 'wk' if x < 1024 else ('reg' if x >= 1024 and x <= 49151 else 'priv'))
    ''' remove majuscule from values in column action'''
    log_data['action'] = log_data['action'].str.upper()

    return log_data
## Create dataset

def create_merge_IPsrc(log_data):

    # Groupby total
    IPsrc_grouped = log_data.groupby('IPsrc')['IPdst'].count().sort_values(ascending=False)
    IPsrc_grouped = pd.DataFrame([IPsrc_grouped.index,IPsrc_grouped]).transpose()
    IPsrc_grouped.columns = ['IPsrc', 'count']

    # Groupby deny
    IPsrc_deny = log_data[log_data.action == 'DENY'].groupby('IPsrc')['IPdst'].count().sort_values(ascending=False)
    IPsrc_deny = pd.DataFrame([IPsrc_deny.index,IPsrc_deny]).transpose()
    IPsrc_deny.columns = ['IPsrc', 'count']

    # Groupby permit
    IPsrc_permit = log_data[log_data.action == 'PERMIT'].groupby('IPsrc')['IPdst'].count().sort_values(ascending=False)
    IPsrc_permit = pd.DataFrame([IPsrc_permit.index,IPsrc_permit]).transpose()
    IPsrc_permit.columns = ['IPsrc', 'count']

    # Merge dataframes
    Merge_IPsrc = pd.merge(IPsrc_grouped,IPsrc_deny, on='IPsrc', how='outer')
    Merge_IPsrc = pd.merge(Merge_IPsrc,IPsrc_permit, on='IPsrc', how='outer')

    # Rename columns
    Merge_IPsrc.columns = ['IPsrc', 'total', 'deny', 'permit']

    # Fill NaN values
    Merge_IPsrc['deny'] = Merge_IPsrc['deny'].fillna(0)
    Merge_IPsrc['permit'] = Merge_IPsrc['permit'].fillna(0)

    # Convert total to int64
    Merge_IPsrc['total'] = Merge_IPsrc.total.astype('int64')

    # Calculate ratio
    Merge_IPsrc['ratio'] = Merge_IPsrc['deny'] / Merge_IPsrc['total']

    # Return dataframe
    return Merge_IPsrc


# create classes for ratio
def ratio_class(x):
    if x < 0.1:
        return '0-10%'
    elif x < 0.2:
        return '10-20%'
    elif x < 0.3:
        return '20-30%'
    elif x < 0.4:
        return '30-40%'
    elif x < 0.5:
        return '40-50%'
    elif x < 0.6:
        return '50-60%'
    elif x < 0.7:
        return '60-70%'
    elif x < 0.8:
        return '70-80%'
    elif x < 0.9:
        return '80-90%'
    else:
        return '90-100%'    

# create ratio_count dataframe
def ratio_count_df(grp_df):
    ratio_count = grp_df.groupby('ratio')['IPsrc'].count()
    ratio_count = pd.DataFrame([ratio_count.index,ratio_count]).transpose()
    ratio_count.columns = ['ratio', 'count']
    ratio_count['class'] = ratio_count.ratio.apply(ratio_class)
    ratio_count.sort_values(by='ratio', ascending=False)
    return ratio_count

# Create graph

def plot_pie(df, col):
    pie = px.pie(df.head(10), values=col, names='IPsrc', title='Nombre total de requêtes {} par IP Source'.format(col),width=500, height=500)
    return pie
#filtre/permit/denied

def plot_scatter(df, col1, col2):
    scatter = px.scatter(df, x=col1, y=col2, title='Nombre total de requêtes par IP Source', 
                 hover_name='IPsrc', size='total', size_max=60, color='ratio', color_continuous_scale=px.colors.sequential.RdBu_r,width=1100, height=700)
    scatter.update_layout(xaxis=dict(rangeslider=dict(visible=True),
                             type="linear"))
    return scatter

# create function to plot previous pie chart

def plot_pie_ratio(df, col):
    pie = px.pie(df, values=col,width=500, height=500, names='class',title='Ratio de requêtes refusées par IP Source', category_orders={'class': ['90-100%', '80-90%', '70-80%', '60-70%', '50-60%', '40-50%', '30-40%', '20-30%', '10-20%', '0-10%']})
    return pie