from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
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
    """Lista todos os jogadores cadastrados"""
    jogadores = jogador_crud.get_jogadores(db, limit=limit)
    return jogadores

@router.get("/by-name/{nome_jogador}", response_model=schemas.JogadorResponse)
def obter_jogador_por_nome(nome_jogador: str, tag_line: Optional[str] = Query(None), db: Session = Depends(get_db)):
    """
    Retorna os dados de um jogador a partir do seu nome e tag.
    """
    jogador = jogador_crud.get_jogador_by_nome(db, nome_jogador, tag_line)
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return jogador

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