import requests
import pandas as pd


def sqmeterprice_data():
    df_sqmeter=pd.read_csv('/Users/Tomas/code/adriendelorge/TheBurst/raw_data/prixm2-loyer-communes-2019.csv')

    df_sqmeter = df_sqmeter.sort_values(by = 'INSEE_COM').reset_index().drop(columns=['NOM_COM_M','X','ID','index','INSEE_DEP','INSEE_REG','POPULATION','Nb_Ventes','PrixMoyen_M2_1819', 'loyer_apparts', 'loyer_maisons', 'R2appart', 'R2maison', 'CODE_EPCI' ])
    df_sqmeter.columns.values[0]= 'code_commune_INSEE'

    return df_sqmeter
