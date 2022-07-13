import os
from google.oauth2 import service_account
from google.cloud import bigquery

def get_three_cities(employees,budget,dist_airplane,dist_train,quality,subsidies):
    #connection to database
    pathjson="../../the-burst-686e65a94dd6.json"
    CREDENTIAL_KEY = os.getenv('CREDENTIAL_KEY')
    credentials = service_account.Credentials.from_service_account_file(pathjson)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    query1=f"""SELECT * FROM `the-burst.database_cities.testfrenchcities` WHERE Distance_x < {dist_airplane}
    AND Distance_y < {dist_train}"""
    query_job = client.query(query1)
    results = query_job.result()
    df=results.to_dataframe()
    if subsidies == 'Yes':
        df=df[df['statut']==1]
    df['scorelifelevel']= df['PrixMoyen_M2']/14803
    if quality == 'high':
        df['weightedscorelifelevel']= df['scorelifelevel']
    if quality == 'medium':
        df['weightedscorelifelevel'] = df['scorelifelevel']*df['scorelifelevel']
    if quality == 'low' :
        df['weightedscorelifelevel'] = df['scorelifelevel']*df['scorelifelevel']*df['scorelifelevel']
    df=df[df['PrixMoyen_M2']!=0]
    df=df.sort_values(by='weightedscorelifelevel',ascending=False)
    df=df.head(3)
    for i in range(len(df)):
        df['coordinates'].iloc[i]=tuple(str(df['coordinates'].iloc[i]).replace('(','').replace(')','').split(","))
    return df

get_three_cities(100,300000,100,40,'high','Yes')
