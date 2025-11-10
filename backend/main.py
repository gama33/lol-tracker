from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

from fastapi import FastAPI 
from . import riot_api 
from . import models  
from . import schemas 
from .database import SessionLocal, engine 
from sqlalchemy.orm import Session
from fastapi import Depends

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
@app.get("/")
def ler_raiz():
    dados_das_partidas = riot_api.get_partidas_id(riot_api.get_puuid(riot_api.nome_jogador, riot_api.tag_line, riot_api.API_KEY), riot_api.API_KEY, 5)
    return dados_das_partidas
def get_db():
    db = SessionLocal()  
    try:
        yield db  
    finally:
        db.close()

@app.post("/sincronizar-partidas")
def sincronizar_partida(db: Session = Depends(get_db)):

    jogador = db.query(models.Jogador).filter(
        models.Jogador.nome_jogador == riot_api.nome_jogador
    ).first()

    if not jogador:
        puuid = riot_api.get_puuid(riot_api.nome_jogador, riot_api.tag_line, riot_api.API_KEY)
        jogador = models.Jogador(
            puuid=puuid,
            nome_jogador=riot_api.nome_jogador,
            icone_id=0,
        )
        db.add(jogador)
        db.commit()
        db.refresh(jogador)

    historico_partida = riot_api.get_partidas_id(jogador.puuid, riot_api.API_KEY, 5)
    for partida_id in historico_partida:

        partida_existente = db.query(models.Partida).filter(
            models.Partida.partida_id == partida_id
        ).first()

        if partida_existente:
            continue
        
        lista_jogadores = riot_api.get_lista_participantes(partida_id)
        dados_jogador = riot_api.get_jogador_dados(lista_jogadores, jogador.puuid, partida_id)
        nova_partida = models.Partida(**dados_jogador)
        nova_partida.jogador_id = jogador.id

        db.add(nova_partida)
        db.commit()
        db.refresh(nova_partida)

    return {'status': 'Partidas sincronizadas com sucesso'}

@app.post("/sincronizar-jogadores")
def sincronizar_jogadores(jogador: schemas.JogadorCreate, db: Session = Depends(get_db)):
    novo_jogador = models.Jogador(**jogador)
    db.add(novo_jogador)
    db.commit()
    db.refresh(novo_jogador)
    return {"status": "Jogador sincronizado com sucesso", "jogador_id": novo_jogador.id}

@app.get('/partidas')
def ler_partidas(db: Session = Depends(get_db)):
    partidas = db.query(models.Partida).all()
    return partidas