from typing import List, Optional
from collections import Counter
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.crud import partida_crud, jogador_crud

def calcular_estatisticas_jogador(
        db: Session,
        jogador_id: int,
        tipo_fila: Optional[int] = None
) -> schemas.EstatisticasJogador:
    jogador = jogador_crud.get_jogador_by_id(db, jogador_id)

    if not jogador:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Jogador {jogador_id} não encontrado"
        )
    
    participacoes = partida_crud.get_participacoes_by_jogador(db, jogador_id, tipo_fila)

    if not participacoes:
        return schemas.EstatisticasJogador(
            jogador_id=jogador_id,
            nome_jogador=jogador.nome_jogador,
            total_partidas=0,
            total_vitorias=0,
            total_derrotas=0,
            winrate=0.0,
            kda_medio=0.0,
            abates_medio=0.0,
            mortes_medio=0.0,
            assistencias_medio=0.0,
            cs_medio=0.0,
            dano_medio=0,
            ouro_medio=0
        )
    
    total = len(participacoes)
    vitorias = sum(1 for p in participacoes if p.resultado)
    derrotas = total - vitorias

    return schemas.EstatisticasJogador(
        jogador_id=jogador_id,
        nome_jogador=jogador.nome_jogador,
        total_partidas=total,
        total_vitorias=vitorias,
        total_derrotas=derrotas,
        winrate=vitorias / total if total > 0 else 0.0,
        kda_medio=sum(p.kda for p in participacoes) / total,
        abates_medio=sum(p.abates for p in participacoes) / total,
        mortes_medio=sum(p.mortes for p in participacoes) / total,
        assistencias_medio=sum(p.assistencias for p in participacoes) / total,
        cs_medio=sum(p.cs for p in participacoes) / total,
        dano_medio=int(sum(p.dano_campeoes for p in participacoes) / total),
        ouro_medio=int(sum(p.ouro_ganho for p in participacoes) / total),
        top_campeoes=calcular_top_campeoes(participacoes),
        posicoes=calcular_distribuicao_posicoes(participacoes)
    )

def calcular_top_campeoes(
    participacoes: List[models.Participacao],
    top: int = 5
) -> List[dict]:
    campeoes = Counter(p.campeao for p in participacoes)

    resultado = []
    for campeao, quantidade in campeoes.most_common(top):
        participacoes_campeao = [p for p in participacoes if p.campeao == campeao]
        vitorias = sum(1 for p in participacoes_campeao if p.resultado)

        resultado.append({
            'campeao': campeao,
            'partidas': quantidade,
            'vitorias': vitorias,
            'derrotas': quantidade - vitorias,
            'winrate': vitorias / quantidade if quantidade > 0 else 0.0,
            'kda_medio': sum(p.kda for p in participacoes_campeao) / quantidade,
        })
    
    return resultado

def calcular_distribuicao_posicoes(participacoes: List[models.Participacao]) -> dict:
    posicoes = Counter(p.posicao for p in participacoes if p.posicao)
    total = sum(posicoes.values())

    return{
        posicao: {
            'partidas': quantidade,
            'perentual': (quantidade / total * 100) if total > 0 else 0
        }
        for posicao, quantidade in posicoes.items()
    }