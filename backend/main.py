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
    dados_das_partidas = riot_api.get_partidas_id(riot_api.get_puuid(riot_api.nome_jogador, riot_api.tag_line, riot_api.API_KEY), riot_api.API_KEY, 5)
    return dados_das_partidas

# aqui criamos uma função de dependência para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()  
    try:
        yield db  
    finally:
        db.close()  

@app.post("/sincronizar-partida") # criação da rota POST
def sincronizar_partida(db: Session = Depends (get_db)): # "quando alguém acessar essa rota, execute a função get_db e me retorne o resultado da variável db"
    puuid = riot_api.get_puuid(riot_api.nome_jogador, riot_api.tag_line, riot_api.API_KEY)
    historico_partida = riot_api.get_partidas_id(puuid, riot_api.API_KEY, 5)

    for partida_id in historico_partida:
        lista_jogadores = riot_api.get_lista_participantes(partida_id)
        dados_jogador = riot_api.get_jogador_dados(lista_jogadores, puuid, partida_id)

        # 1. cria um objeto Partida com dados puxados da API
        nova_partida = models.Partida(**dados_jogador) #O FastAPI tem um atalho muito útil. Se as chaves do seu dicionário ('campeao', 'abates', etc.) forem exatamente iguais aos nomes dos campos no seu models.Partida, você pode usar o operador ** (dois asteriscos) para "desempacotar" o dicionário

        print(f"Salvando dados para: {nova_partida.campeao}")

        # 2. adiciona o objeto à sessão (prepara para salvar)
        db.add(nova_partida)

        # 3. confirma a transação (salva de verdade no banco)
        db.commit()

        # 4. atualiza o objeto com os dados do banco (com o ID gerado)
        db.refresh(nova_partida)

    return {'status': 'Partidas sincronizadas com sucesso'}