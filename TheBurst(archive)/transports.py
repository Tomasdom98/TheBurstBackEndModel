import requests
import pandas as pd
import xlrd
from TheBurst.cities_data import get_cities_data
from TheBurst.utils import haversine, coord_converter

def get_airport_data():
    df_airports=pd.read_excel('/Users/Tomas/code/adriendelorge/TheBurst/raw_data/airports.xls', skiprows=[0,1])
    w_header = df_airports.iloc[0] #grab the first row for the header #take the data less the header row
    df_airports.columns = w_header #set the header row as the df header
    df_airports = df_airports.drop(labels=0, axis=0)
    df_bigairports=df_airports[df_airports['Code IATA'].isin(['CDG','ORY','LYS','MRS','TLS','BSL','MLH','EAP','BOD','NTE','BVA','PTP','RUN','LIL','FDF','MPL','AJA','BIA','PPT','SXB','BES','BIQ','RNS','FSC','PUF','NOU','CAY','TLN','LDE','GEA','PGF','CFE'])]
    df_bigairports.reset_index(inplace=True)
    df_bigairports.columns.values[4] = 'Latitude'
    df_bigairports.columns.values[5] = 'Longitude'
    df_bigairports.iloc[:,4] = df_bigairports.iloc[:,4].apply(lambda x: coord_converter(x))
    df_bigairports.iloc[:,5] = df_bigairports.iloc[:,5].apply(lambda x: coord_converter(x))
    df_bigairports['coordinates'] = tuple(zip(df_bigairports.iloc[:,4],df_bigairports.iloc[:,5]))
    disonecity=[]
    cityname=[]
    aptname=[]
    df_cities=get_cities_data()
    for coords,airport in zip(df_bigairports.coordinates, df_bigairports['Nom aéroport']):
        for coords2,city in zip(df_cities['coordinates'], df_cities.code_commune_INSEE):
            disonecity.append(haversine(coords,coords2))
            cityname.append(city)
            aptname.append(airport)
    d={'code_commune_INSEE':cityname,'Airport':aptname,'Distance':disonecity}
    df_cityairport=pd.DataFrame(d)
    df_cityairport.dropna(subset=['Distance'],inplace=True)
    df_distance=df_cityairport[['code_commune_INSEE','Airport','Distance']].groupby(['code_commune_INSEE'])['Distance'].min().to_frame()
    df_distance=df_distance.merge(df_cityairport,on='Distance',how='left')
    return df_distance

def get_train_data():
    df_train=pd.read_excel('/Users/Tomas/code/adriendelorge/TheBurst/raw_data/train.xls')
    df_train['coordinates'] = df_train['WGS 84'].apply(lambda x: tuple(map(str, x.split(', '))))
    lattrain=[]
    lontrain=[]
    for x in df_train.coordinates:
        lattrain.append(float(x[0]))
        lontrain.append(float(x[1]))
    df_train['Latitude']=lattrain
    df_train['Longitude']=lontrain
    df_train['coordinates'] = tuple(zip(df_train['Latitude'],df_train['Longitude']))
    disonecity2=[]
    cityname2=[]
    aptname2=[]
    df_cities=get_cities_data()
    for coords,train in zip(df_train.coordinates, df_train['UT']):
        for coords2,city in zip(df_cities['coordinates'], df_cities.code_commune_INSEE):
            disonecity2.append(haversine(coords,coords2))
            cityname2.append(city)
            aptname2.append(train)
    d2={'code_commune_INSEE':cityname2,'Train':aptname2,'Distance':disonecity2}
    df_citytrain=pd.DataFrame(d2)
    df_citytrain.dropna(subset=['Distance'],inplace=True)
    df_distance2=df_citytrain[['code_commune_INSEE','Train','Distance']].groupby(['code_commune_INSEE'])['Distance'].min().to_frame()
    df_distance2=df_distance2.merge(df_citytrain,on='Distance',how='left')
    return df_distance2
