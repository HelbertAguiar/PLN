import json, requests, pprint, base64

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

url_api = 'https://api.gotit.ai/NLU/v1.5/Analyze'
key_identifier = "XXXXX" # Buscar no site a API_kEY
key_secret = "YYYYY" # Buscar no site a API_kEY

api = api_pln(url_api, key_identifier, key_secret)

msg = "Victor comeu uma pizza horrivel."
# msg = "meu deus não acredito"

response = api.consulta(msg)
pprint.pprint(response.json())

