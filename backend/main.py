from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
import time
from . import riot_api, models, schemas
from .database import SessionLocal, engine 

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LOL Tracker API",
    description="API para rastreae e analisar partidas de League of Legends",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173", "http://localhost:3000"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def buscar_ou_criar_jogador(
    db: Session,
    nome_jogador: str,
    tag_line: str
) -> models.Jogador:
    
    jogador = db.query(models.Jogador).filter(
        models.Jogador.nome_jogador == nome_jogador
    ).first()
    
    if jogador:
        return jogador
    
    try:
        puuid = riot_api.get_puuid(nome_jogador, tag_line)
        
        novo_jogador = models.Jogador(
            puuid=puuid,
            nome_jogador=nome_jogador,
            icone_id=0,
            nivel=1
        )
        
        db.add(novo_jogador)
        db.commit()
        db.refresh(novo_jogador)
        
        return novo_jogador
        
    except riot_api.RiotAPIException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao buscar jogador na Riot API: {e.message}"
        )

def sincronizar_partida_completa(
    db: Session,
    match_id: models.Jogador,
    jogador: models.Jogador
) -> tuple[models.Partida, models.Participacao]:
    
    partida = db.query(models.Partida).filter(
        models.Partida.partida_id == match_id
    ).first()

    if not partida:
        try:
            dados_partida = riot_api.get_dados_partida(match_id)
            partida = models.Partida(**dados_partida)
            db.add(partida)
            db.commit()
            db.refresh(partida)
        except riot_api.RiotAPIException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"erro ao buscar dados da partida: {e.message}"
            )
        
    participacao = db.query(models.Participacao).filter(
        models.Participacao.jogador_id == jogador.id,
        models.Participacao.partida_id == partida.id
    ).first()

    if participacao:
        return partida, participacao
    
    try:
        dados_participacao = riot_api.get_dados_participacao(match_id, jogador.puuid)

        participacao = models.Participacao(
            jogador_id = jogador.id,
            partida_id = partida.id,
            **dados_participacao
        )
        
        db.add(participacao)
        db.commit()
        db.refresh(participacao)

        return partida, participacao
    
    except riot_api.RiotAPIException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"erro ao buscar participação: {e.message}"
        )

