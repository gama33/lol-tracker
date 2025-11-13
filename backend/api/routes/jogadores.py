from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend import schemas
from backend.core.dependencies import get_db
from backend.services import jogador_service, estatisticas_service
from backend.crud import jogador_crud

router = APIRouter(prefix="/jogadores", tags=["jogadores"])

@router.get("", response_model=List[schemas.JogadorResponse])
def listar_jogadores(
    limit: int = Query(50, ge=1, le=100, description="Limite de resultados"),
    db: Session = Depends(get_db)
):
    jogador = jogador_crud.get_jogadores(db, limit=limit)

    response = schemas.JogadorResponse.model_validate(jogador)
    response.total_partidas = jogador.total_partidas
    response.total_vitorias = jogador.total_vitorias
    response.winrate = jogador.winrate

    return response

@router.get("/{jogador_id}/estatisticas", response_model=schemas.EstatisticasJogador)
def obter_estatisticas(
    jogador_id: int,
    tipo_fila: int | None = Query(None, description="Filtro por tipo de fila"),
    db: Session = Depends(get_db)
):
    return estatisticas_service.calcular_estatisticas_jogador(
        db,
        jogador_id,
        tipo_fila
    )