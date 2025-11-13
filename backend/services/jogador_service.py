from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend import riot_api, models
from backend.crud import jogador_crud

def buscar_ou_criar_jogador(
    db: Session,
    nome_jogador: str,
    tag_line: str
) -> models.Jogador:
    jogador = jogador_crud.get_jogador_by_nome(db, nome_jogador)

    if jogador:
        try:
            dados_summoner = riot_api.get_dados_summoner(jogador.puuid)
            jogador = jogador_crud.update_jogador_info(
                db,
                jogador,
                icone_id=dados_summoner['icone_id'],
                nivel=dados_summoner['nivel']
            )
        except riot_api.RiotAPIException:
            pass
        
        return jogador

    try:
        puuid = riot_api.get_puuid(nome_jogador, tag_line)

        dados_summoner = riot_api.get_dados_summoner(puuid)

        novo_jogador = jogador_crud.create_jogador(
            db,
            puuid=puuid,
            nome_jogador=nome_jogador,
            icone_id=dados_summoner['icone_id'],
            nivel=dados_summoner['nivel']
        )

        return jogador

    except riot_api.RiotAPIException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao buscar jogador na Riot API: {e.message}"
        )
    
def obter_jogador(db: Session, jogador_id: int) -> models.Jogador:
    jogador = jogador_crud.get_jogador_by_id(db, jogador_id)

    if not jogador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogador {jogador_id} não encontrado"
        )
    
    return jogador