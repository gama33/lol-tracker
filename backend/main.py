# esse arquivo tem a "preocupação" de definir as rotas da aplicação
# importar a classes
from fastapi import FastAPI # importa o modulo FastAPI
import riot_api # importa o modulo riot_api
import models # importa o modelo do banco de dados 
from database import SessionLocal, engine # importa a engine do banco de dados e a sessão local
from sqlalchemy.orm import Session
from fastapi import Depends

# aqui o código diz ao SQLAlchemy para cirar as tabelas no banco de dados definidas em models.py
models.Base.metadata.create_all(bind=engine) # cria as tabelas no banco de dados

# criar uma instância da aplicação
app = FastAPI()

# define a rota principal (endpoint)
@app.get("/")
def ler_raiz():
    dados_das_partidas = riot_api.get_partidas_ids(riot_api.puuid, riot_api.API_KEY)
    return dados_das_partidas

# aqui criamos uma função de dependência para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()  
    try:
        yield db  
    finally:
        db.close()  

@app.post("/sincronizar-partida-exemplo/") # criação da rota POST
def sincronizar_partida(db: Session = Depends (get_db)): # "quando alguém acessar essa rota, execute a função get_db e me retorne o resultado da variável db"
    # 1. cria um objeto Partida com dados de exemplo
    partida_exemplo = models.Partida(
        campeao="Jinx",
        abates=10,
        mortes=2,
        assistencias=8,
        cs=250
    )

    # 2. adiciona o objeto à sessão (prepara para salvar)
    db.add(partida_exemplo)

    # 3. confirma a transação (salva de verdade no banco)
    db.commit()

    # 4. atualiza o objeto com os dados do banco (com o ID gerado)
    db.refresh(partida_exemplo)

    return partida_exemplo