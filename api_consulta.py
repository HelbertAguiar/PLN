import json, requests, base64, datetime
import pandas as pd

# Documentacao API Postman
# https://documenter.getpostman.com/view/4456678/RWaHyVMX

# Site de apresentacao da API:
# https://www.gotit.ai/

class api_pln(object):

    def __init__(self, url_api, key_identifier, key_secret):
        self.url_api = url_api
        self.key_identifier = key_identifier
        self.key_secret = key_secret
    
    def consulta(self, texto, analise_sentimento = True, analise_emocoes = True, analise_entidade = True):
        
        data = {"T":texto,"S":analise_sentimento, "EM":analise_emocoes, "E":analise_entidade}
        data_json = json.dumps(data)
        pwd = "{}:{}".format(self.key_identifier, self.key_secret)
        pwd = bytes(pwd, encoding='utf-8')
        userAndPass = base64.b64encode(pwd).decode("ascii")
        headers = {'Content-type': 'application/json', "Authorization": "Basic %s" %  userAndPass}
        return requests.post(self.url_api, data=data_json, headers=headers)
        

def open_dataframe_and_addcolumns(path_file_tweets_preprocessed):
    df = pd.read_csv(path_file_tweets_preprocessed)
    df['Sentimento_Score'] = "Null"
    df['Sentimento_Label'] = "Null"
    df['Tristeza'] = "Null"
    df['Alegria'] = "Null"
    df['Medo'] = "Null"
    df['Desgosto'] = "Null"
    df['Raiva'] = "Null"
    return df

url_api = 'https://api.gotit.ai/NLU/v1.5/Analyze'

# Buscar no site a API_kEY
key_identifier = "2147-8fs6d1E/" 
# Buscar no site a API_kEY
key_secret = "DXKm42YCBxReVKU7UDW7TAt2FpEvu/cx" 

# Arquivos de leitura e saida
path_file_tweets_preprocessed = "./preprocessed_tweets.csv"
path_file_tweets_PLN = "./preprocessed_tweets_PLN.csv" 

# Adiciona colunas da PLN ao dataset
df = open_dataframe_and_addcolumns(path_file_tweets_preprocessed) 
api = api_pln(url_api, key_identifier, key_secret)

# executando analise
print("Inicio: " + str(datetime.datetime.now()))
cont = 0

# percorre linhas do dataframe e consulta API na mensagem 
for i in range(len(df)) :
    msg = df.loc[i, "text"]
    response = (api.consulta(msg)).json()
    df.loc[i, "Sentimento_Score"] = response['sentiment']['score']
    df.loc[i, "Sentimento_Label"] = response['sentiment']['label']
    df.loc[i, "Tristeza"] = response['emotions']['sadness']
    df.loc[i, "Alegria"] = response['emotions']['joy']
    df.loc[i, "Medo"] = response['emotions']['fear']
    df.loc[i, "Desgosto"] = response['emotions']['disgust']
    df.loc[i, "Raiva"] = response['emotions']['anger']
    cont = cont + 1
    print("Processado msg nr {}: ".format(cont) + str(datetime.datetime.now()))

print("Fim:    " + str(datetime.datetime.now()))

# salva o arquivo com as colunas da analise
df.to_csv(path_file_tweets_PLN, index=False, header=True, encoding='utf-8', mode='a')