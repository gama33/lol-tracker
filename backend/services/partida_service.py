from typing import Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend import riot_api, models
from backend.crud import partida_crud

def sincronizar_partida_completa(
    db: Session,
    match_id: str,
    jogador: models.Jogador
) -> Tuple[models.Partida, models.Participacao]:
    partida = partida_crud.get_partida_by_match_id(db, match_id)

    if not partida:
        try:
            dados_partida = riot_api.get_dados_partida(match_id)

            partida = partida_crud.create_partida(db, **dados_partida)

        except riot_api.RiotAPIException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao buscar dados da partida: {e.message}"
            )
        
    participacao = partida_crud.get_participacao(db, jogador.id, partida.id)

    if participacao:
        return partida, participacao
    
    try:
        dados_participacao = riot_api.get_dados_participacao(match_id, jogador.puuid)

        participacao = partida_crud.create_participacao(
            db,
            jogador_id=jogador.id,
            partida_id=partida.id,
            dados_participacao=dados_participacao
        )

        return partida, participacao
    
    except riot_api.RiotAPIException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao buscar participacoes: {e.message}"
        )
    
def verificar_partida_ja_sincronizada(
    db: Session,
    match_id: str,
    jogador_id: int
) -> bool:
    partida = partida_crud.get_partida_by_match_id(db, match_id)

    if not partida:
        return False
    
    participacao = partida_crud.get_participacao(db, jogador_id, partida.id)

    return participacao is not None