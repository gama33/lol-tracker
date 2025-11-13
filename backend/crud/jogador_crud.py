from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend import models

def get_jogador_by_id(db: Session, jogador_id: int) -> Optional[models.Jogador]:
    return db.query(models.Jogador).filter(
        models.Jogador.id == jogador_id
    ).first()

def get_jogador_by_nome(db: Session, nome_jogador: str) -> Optional[models.Jogador]:
    return db.query(models.Jogador).filter(
        models.Jogador.nome_jogador == nome_jogador
    ).first()

def get_jogador_by_puuid(db: Session, puuid: str) -> Optional[models.Jogador]:
    return db.query(models.Jogador).filter(
        models.Jogador.puuid == puuid
    ).first()

def get_jogadores(db: Session, skip: int = 0, limit: int = 50) -> List[models.Jogador]:
    return db.query(models.Jogador).offset(skip).limit(limit).all()

def create_jogador(
    db: Session,
    puuid: str,
    nome_jogador: str,
    icone_id: int,
    nivel: int
) -> models.Jogador:
    
    jogador = models.Jogador(
        puuid=puuid,
        nome_jogador=nome_jogador,
        icone_id=icone_id,
        nivel=nivel
    )
    db.add(jogador)
    db.commit()
    db.refresh(jogador)
    return jogador

def update_jogador_info(
    db: Session,
    jogador: models.Jogador,
    icone_id: int,
    nivel: int
) -> models.Jogador:
    jogador.icone_id = icone_id
    jogador.nivel = nivel
    db.commit()
    db.refresh(jogador)
    return jogador