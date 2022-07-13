import requests
import pandas as pd
import xlrd

def subsidies():
    df_subsidies = pd.read_excel('/Users/Tomas/code/adriendelorge/TheBurst/raw_data/diffusion-zonages-afr-cog2021.xls')
    df_subsidies.columns = ['code_commune_INSEE','nom','statut']
    df_subsidies= df_subsidies.drop(df_subsidies.index[[0,1,2,3,4]])
    df_subsidies= df_subsidies.drop(columns = ['nom'])
    df_subsidies = df_subsidies.reset_index()
    df_subsidies.drop(columns = 'index')

    for x in range(len(df_subsidies['statut'])): #putting a 1 if the city gives subsidies
        if df_subsidies['statut'].iloc[x] == 'NC - Non éligible':
            df_subsidies['statut'].iloc[x] = 0
        else :
            df_subsidies['statut'].iloc[x] = 1

    return df_subsidies
