# esse arquivo tem a "preocupação" de definir as rotas da aplicação
# importar a classes
from fastapi import FastAPI # importa o modulo FastAPI
from . import riot_api # importa o modulo riot_api

# criar uma instância da aplicação
app = FastAPI()

# define a rota principal (endpoint)
@app.get("/")
def ler_raiz():
    dados_das_partidas = riot_api.get_partidas_ids(riot_api.puuid, riot_api.API_KEY)
    return dados_das_partidas