from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend import models

def get_partida_by_id(db: Session, partida_id: int) -> Optional[models.Partida]:
    return db.query(models.Partida).filter(
        models.Partida.id == partida_id
    )

def get_partida_by_match_id(db: Session, match_id: str) -> Optional[models.Partida]:
    return db.query(models.Partida).filter(
        models.Partida.partida_id == match_id
    ).first()

def get_partidas(
    db: Session,
    jogador_id: Optional[int] = None,
    tipo_fila: Optional[int] = None,
    skip: int = 0,
    limit: int = 20
) -> List[models.Partida] | List[tuple[models.Partida, models.Participacao]]:
    
    if jogador_id:
        query = db.query(models.Partida, models.Participacao)\
            .join(models.Participacao, models.Partida.id == models.Participacao.partida_id)\
            .filter(models.Participacao.jogador_id == jogador_id)
    else:
        query = db.query(models.Partida)

    if tipo_fila:
        query = query.filter(models.Partida.tipo_fila == tipo_fila)

    query = query.order_by(desc(models.Partida.data_partida))

    return query.offset(skip).limit(limit).all()

def create_partida(
    db: Session,
    partida_id: str,
    data_partida: int,
    duracao_partida: int,
    tipo_fila: int,
    patch: str
) -> models.Partida:
    
    partida = models.Partida(
        partida_id=partida_id,
        data_partida=data_partida,
        duracao_partida=duracao_partida,
        tipo_fila=tipo_fila,
        patch=patch
    )

    db.add(partida)
    db.commit()
    db.refresh(partida)
    return partida

def get_participacao(
    db: Session,
    jogador_id: int,
    partida_id: int
) -> Optional[models.Participacao]:
    
    return db.query(models.Participacao).filter(
        models.Participacao.jogador_id == jogador_id,
        models.Participacao.partida_id == partida_id
    ).first()

def get_participacoes_by_jogador(
    db: Session,
    jogador_id: int,
    tipo_fila: Optional[int] = None
) -> List[models.Participacao]:
    
    query = db.query(models.Participacao).filter(
        models.Participacao.jogador_id == jogador_id
    )

    if tipo_fila is not None:
        query = query.join(models.Partida).filter(
            models.Partida.tipo_fila == tipo_fila
        )

    return query.all()

def create_participacao(
    db: Session,
    jogador_id: int,
    partida_id: int,
    dados_participacao: dict
) -> models.Participacao:
    
    participacao = models.Participacao(
        jogador_id=jogador_id,
        partida_id=partida_id,
        **dados_participacao
    )

    db.add(participacao)
    db.commit()
    db.refresh(participacao)
    return participacao