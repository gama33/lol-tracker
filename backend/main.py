# esse arquivo tem a "preocupação" de definir as rotas da aplicação
# importar a classes
from fastapi import FastAPI # importa o modulo FastAPI
import riot_api # importa o modulo riot_api
import models # importa o modelo do banco de dados 
from database import engine # importa a engine do banco de dados

# aqui o código diz ao SQLAlchemy para cirar as tabelas no banco de dados definidas em models.py
models.Base.metadata.create_all(bind=engine) # cria as tabelas no banco de dados

# criar uma instância da aplicação
app = FastAPI()

# define a rota principal (endpoint)
@app.get("/")
def ler_raiz():
    dados_das_partidas = riot_api.get_partidas_ids(riot_api.puuid, riot_api.API_KEY)
    return dados_das_partidas