import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend import riot_api, schemas
from backend.core.dependencies import get_db
from backend.services import jogador_service, partida_service

router = APIRouter(prefix="/sincronizar-partidas", tags=["Sincronização"])

@router.post("", response_model=schemas.SincronizarPartidaResponse)
def sincronizar_partidas(
    request: schemas.SincronizarPartidaRequest,
    db: Session = Depends(get_db)
):
    inicio = time.time()

    nome = request.nome_jogador or riot_api.nome_jogador
    tag = request.tag_line or riot_api.tag_line

    try:
        jogador = jogador_service.buscar_ou_criar_jogador(db, nome, tag)

        queue_filter = 420 if request.apenas_ranked else None

        try:
            match_ids = riot_api.get_partidas_id(
                jogador.puuid,
                count=request.quantidade,
                queue=queue_filter
            )
        except riot_api.RiotAPIException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao buscar histórico: {e.message}"
            )
        
        sincronizadas = 0
        duplicadas = 0
        erros = []

        for match_id in match_ids:
            try:
                if partida_service.verificar_partida_ja_sincronizada(
                    db, match_id, jogador.id
                ):
                    duplicadas += 1
                    continue

                partida_service.sincronizar_partida_completa(db, match_id, jogador)
                sincronizadas += 1

            except HTTPException as e:
                erros.append(f"{match_id}: {e.detail}")
            except Exception as e:
                erros.append(f"{match_id}: {str(e)}")
        
        tempo_total = time.time() - inicio

        return schemas.SincronizarPartidaResponse(
            status="sucesso" if sincronizadas > 0 else "nenhuma_partida_nova",
            partidas_sincronizadas=sincronizadas,
            partidas_duplicadas=duplicadas,
            erros=erros,
            tempo_execucao=round(tempo_total, 2)  
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado: {str(e)}"
        )