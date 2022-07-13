from fastapi import FastAPI
import os
from google.oauth2 import service_account
from google.cloud import bigquery
from dotenv import load_dotenv, find_dotenv
import json

app = FastAPI()

   # define a root `/` endpoint
@app.get("/")

def get_three_cities(employees,budget,dist_airplane,dist_train,quality,subsidies,mountain,sea,sectorimportance,sectorcode):
    # point to .env file
    #env_path = find_dotenv() # automatic find
    #load_dotenv()
    CREDENTIAL_KEY = os.environ.get('CREDENTIAL_KEY')
    credentials = service_account.Credentials.from_service_account_info(json.loads(CREDENTIAL_KEY))
    #connection to database
    #pathjson="/Users/Tomas/Desktop/KEYS/the-burst-b6d61e428faa.json"
    #CREDENTIAL_KEY = os.getenv('CREDENTIAL_KEY')
    #credentials = service_account.Credentials.from_service_account_file(pathjson)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    query1=f"""SELECT * FROM `the-burst.database_cities.testfrenchcities` WHERE Distance_x < {dist_airplane}+5
    AND Distance_y < {dist_train}+5"""
    query_job = client.query(query1)
    results = query_job.result()
    df=results.to_dataframe()
    if subsidies == 'Yes':
        df=df[df['statut']==1]
    if mountain == 'Important':
        df=df[df['mountain_city']==1]
    if sea == 'Important':
        df=df[df['sea_city']==1]
    df['cost']= float(employees)*10*df['PrixMoyen_M2']
    df=df[df['cost']<=float(budget)]
    df['scorelifelevel']= df['lifelevelscore']
    if quality == 'Very_Important':
        df['weightedscorelifelevel']= df['scorelifelevel']
    if quality == 'Important':
        df['weightedscorelifelevel'] = df['scorelifelevel']*df['scorelifelevel']
    if quality == 'Somewhat_Important' :
        df['weightedscorelifelevel'] = df['scorelifelevel']*df['scorelifelevel']*df['scorelifelevel']
    df=df[df['PrixMoyen_M2']!=0]
    sector1 = df['s1'].tolist()
    sector2 = df['s2'].tolist()
    sector3 = df['s3'].tolist()
    sectorsscore = []
    for x in sector1:
        if x == sectorcode:
            sectorsscore.append(10)
        else:
            sectorsscore.append(0)
    sectorsscore2 = []
    for x in sector2:
        if x == sectorcode:
            sectorsscore2.append(6)
        else:
            sectorsscore2.append(0)
    sectorsscore3 = []
    for x in sector3:
        if x == sectorcode:
            sectorsscore3.append(2)
        else:
            sectorsscore3.append(0)
    finalscore = []
    for i in range(len(sectorsscore)):
        total = sectorsscore[i] + sectorsscore2[i] + sectorsscore3[i]
        finalscore.append(total/10)
    df['sectorratio']= finalscore
    if sectorimportance == 'High':
        df['weightedsectorscore']= df['sectorratio']
    if sectorimportance == 'Medium':
        df['weightedsectorscore'] = (df['sectorratio'])*(df['sectorratio'])
    if sectorimportance == 'Low' :
        df['weightedsectorscore'] = (df['sectorratio'])*(df['sectorratio'])*(df['sectorratio'])
    df['finalscore']=df['weightedscorelifelevel']*3+df['weightedsectorscore']
    df=df.sort_values(by='finalscore',ascending=False)
    if len(df)>=3:
        df=df.head(3)
        for i in range(len(df)):
            df['coordinates'].iloc[i]=tuple(str(df['coordinates'].iloc[i]).replace('(','').replace(')','').split(","))
        df[['code_postal','mountain_city','sea_city']]=df[['code_postal','mountain_city','sea_city']].astype(dtype='float64')
        df = df.dropna()
        dit = df.to_dict(orient='list')
        return dit
    else:
        return {'Error':'No such city, expand yor criterias!'}

get_three_cities(100,300000,100,40,'Very_Important','Yes','Important','Important','High','GI')
# /?employees=100&budget=300000&dist_airplane=100&dist_train=40&quality=Very_Important&subsidies=Yes&mountain=Important&sea=Important&sectorimportance=High&sectorcode=GI

@app.get("/cluster")

def get_five_samples(cluster):
    # point to .env file
    #env_path = find_dotenv() # automatic find
    #load_dotenv()
    CREDENTIAL_KEY = os.environ.get('CREDENTIAL_KEY')
    credentials = service_account.Credentials.from_service_account_info(json.loads(CREDENTIAL_KEY))
    #connection to database
    #pathjson="/Users/Tomas/Desktop/KEYS/the-burst-b6d61e428faa.json"
    #CREDENTIAL_KEY = os.getenv('CREDENTIAL_KEY')
    #credentials = service_account.Credentials.from_service_account_file(pathjson)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    query1=f"""SELECT * FROM `the-burst.database_cities.testfrenchcities`"""
    query_job = client.query(query1)
    results = query_job.result()
    df=results.to_dataframe()
    df=df[df['cluster']==float(cluster)]
    df[['code_postal','mountain_city','sea_city']]=df[['code_postal','mountain_city','sea_city']].astype(dtype='float64')
    df = df.dropna()
    sample_df=df.sample(n=5)
    dic = sample_df.to_dict(orient='list')
    return dic

get_five_samples(4)
# /cluster?cluster=4
