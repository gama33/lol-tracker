from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from backend import schemas
from backend.core.dependencies import get_db
from backend.crud import partida_crud

router = APIRouter(prefix="/partidas", tags=["Partidas"])

@router.get("", response_model=List[schemas.PartidaResponse])
def listar_partidas(
    jogador_id: int | None = Query(None, description="Filtrar por jogador"),
    tipo_fila: int | None = Query(None, description="Filtrar por tipo de fila"),
    limit: int = Query(20, ge=1, le=100, description="Limite de resultados"),
    db: Session = Depends(get_db)
):
    results = partida_crud.get_partidas(
        db,
        jogador_id=jogador_id,
        tipo_fila=tipo_fila,
        limit=limit
    )

    if jogador_id:
        partidas_com_participacao = []
        for partida, participacao in results:
            partida_dto = schemas.PartidaResponse.from_orm(partida)
            partida_dto.participacao = schemas.ParticipacaoResponse.from_orm(participacao)
            partidas_com_participacao.append(partida_dto)
        return partidas_com_participacao
    
    return results

@router.get("/{partida_id}", response_model=schemas.ParticipacaoDetalhada)
def obter_partida(
    partida_id: int,
    db: Session = Depends(get_db)
):
    partida = partida_crud.get_participacoes_by_jogador(fb, partida_id)

    if not partida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Partida {partida_id} não encontrada"
        )
    
    return partida

