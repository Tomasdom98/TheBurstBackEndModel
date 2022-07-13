import pandas as pd
import xlrd

def get_cities_data():

    df_cities=pd.read_csv('/Users/Tomas/code/adriendelorge/TheBurst/raw_data/cities.csv')
    df_cities=df_cities[['code_commune_INSEE','code_postal','latitude','longitude','nom_commune_complet','code_departement','nom_departement','code_region','nom_region']]
    df_cities['coordinates'] = tuple(zip(df_cities.latitude,df_cities.longitude))
    df_cities=df_cities.drop_duplicates(subset=['code_commune_INSEE'])
    df_cities.dropna(subset=['nom_departement'],inplace=True)
    df_cities.reset_index(inplace=True)

    pop=pd.read_excel('/Users/Tomas/code/adriendelorge/TheBurst/raw_data/pop.xls')
    pop.rename(columns={'CODGEO':'code_commune_INSEE'},inplace=True)
    pop=pop[['code_commune_INSEE','Population']]

    for x in range(len(df_cities['code_commune_INSEE'])):

        if len(df_cities['code_commune_INSEE'][x])<5:
            y='0'+str(df_cities['code_commune_INSEE'][x])
            df_cities['code_commune_INSEE'].iloc[x]=y
    df_cities=df_cities.merge(pop,on='code_commune_INSEE',how='left')
    df_cities=df_cities[df_cities['Population']<30000]

    return df_cities
