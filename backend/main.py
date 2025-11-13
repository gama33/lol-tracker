from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)
from fastapi import FastAPI, Depends, HTTPException, status, Query
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
import time
from . import riot_api, models, schemas
from .database import engine, get_db, init_db, check_db_connection, get_db_info

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("-- Iniciando LOL Tracker API --")
    
    if check_db_connection():
        print("Conexão com banco de dados estabelecida")
        init_db()
        print("Tabelas verificadas/criadas")
    else:
        print("Falha na conexão com banco de dados")
    
    yield
    
    print("-- Encerrando LOL Tracker API --")

app = FastAPI(
    title="LOL Tracker API",
    description="API para rastrear e analisar partidas de League of Legends",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173", "http://localhost:3000"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

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
    match_id: str,
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
                detail=f"Erro ao buscar dados da partida: {e.message}"
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
            detail=f"Erro ao buscar participação: {e.message}"
        )

def calcular_estatisticas_jogador(
    db: Session,
    jogador_id: int,
    tipo_fila: Optional[int] = None
) -> schemas.EstatisticasJogador:
    
    jogador = db.query(models.Jogador).filter(
        models.Jogador.id == jogador_id
    ).first()

    if not jogador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogador {jogador_id} não encontrado"
        )
    
    query = db.query(models.Participacao).filter(
        models.Participacao.jogador_id == jogador_id
    )

    if tipo_fila is not None:
        query = query.join(models.Partida).filter(
            models.Partida.tipo_fila == tipo_fila
        )

    participacoes = query.all()

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

def calcular_top_campeoes(participacoes: List[models.Participacao], top: int = 5) -> List[dict]:
    from collections import Counter

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
    from collections import Counter

    posicoes = Counter(p.posicao for p in participacoes if p.posicao)
    total = sum(posicoes.values())

    return {
        posicao: {
            'partidas': quantidade,
            'percentual': (quantidade / total * 100) if total > 0 else 0
        }
        for posicao, quantidade in posicoes.items()
    }

@app.get(
    "/", 
    tags=["Health"]
)
def root():
    return {
        "status": "online",
        "api": "LOL Tracker",
        "version": "1.0.0",
        "docs": "/docs",
    }

@app.get(
    "/health",
    tags=["Health"]
)
def health_check():
    db_ok = check_db_connection()

    return {
        "status": "healthy" if db_ok else "unhealthy",
        "api": "online",
        "database": "connected" if db_ok else "disconnected"
    }

@app.get(
    "/db/info",
    tags=["Health"]
)
def database_info():
    return get_db_info()

@app.post(
    "/sincronizar-partidas", 
    response_model=schemas.SincronizarPartidaResponse, 
    tags=["Sincronização"], 
    summary="Sincronizar partidas de um jogador"
)
def sincronizar_partidas(
    request: schemas.SincronizarPartidaRequest,
    db: Session = Depends(get_db)
):
    inicio = time.time()

    nome = request.nome_jogador or riot_api.nome_jogador
    tag = request.tag_line or riot_api.tag_line

    try:
        jogador = buscar_ou_criar_jogador(db, nome, tag)

        queue_filter = 420 if request.apenas_ranked else None

        try:
            match_ids = riot_api.get_partidas_id(
                jogador.puuid,
                count = request.quantidade,
                queue = queue_filter
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
                ja_existe = db.query(models.Participacao).join(
                    models.Partida
                ).filter(
                    models.Partida.partida_id == match_id,
                    models.Participacao.jogador_id == jogador.id
                ).first()

                if ja_existe:
                    duplicadas += 1
                    continue

                sincronizar_partida_completa(db, match_id, jogador)
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
    
@app.get(
    "/jogadores/{jogador_id}",
    response_model=schemas.JogadorResponse,
    tags=["Jogadores"]
)
def obter_jogador(jogador_id: int, db: Session = Depends(get_db)):
    jogador = db.query(models.Jogador).filter(
        models.Jogador.id == jogador_id
    ).first()

    if not jogador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogador {jogador_id} não encontrado"
        )
    
    response = schemas.JogadorResponse.model_validate(jogador)
    response.total_partidas = jogador.total_partidas
    response.total_vitorias = jogador.total_vitorias
    response.winrate = jogador.winrate

    return response

@app.get(
    "/jogadores/{jogador_id}/estatisticas",
    response_model=schemas.EstatisticasJogador,
    tags=["Jogadores"]
)
def obter_estatisticas(
    jogador_id: int,
    tipo_fila: Optional[int] = Query(None, description="Filtro por tipo de fila"),
    db: Session = Depends(get_db)
):
    return calcular_estatisticas_jogador(db, jogador_id, tipo_fila)

@app.get(
    "/partidas",
    response_model=List[schemas.PartidaResponse],
    tags=["Partidas"]
)
def listar_partidas(
    jogador_id: Optional[int] = Query(None, description="Filtrar por jogador"),
    tipo_fila: Optional[int] = Query(None, description="Filtrar por tipo de fila"),
    limit: int = Query(20, ge=1, le=100, description="Limite de resultados"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Partida)

    if jogador_id:
        query = query.join(models.Participacao).filter(
            models.Participacao.jogador_id == jogador_id
        )

    if tipo_fila:
        query = query.filter(models.Partida.tipo_fila == tipo_fila)

    query = query.order_by(desc(models.Partida.data_partida))

    partidas = query.limit(limit).all()

    return partidas

@app.get(
    "/partidas/{partida_id}",
    response_model=schemas.PartidaDetalhada,
    tags=["Partidas"]
)
def obter_partida(partida_id: int, db: Session = Depends(get_db)):
    partida = db.query(models.Partida).filter(
        models.Partida.id == partida_id
    ).first()

    if not partida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Partida {partida_id} não encontrada"
        )
    
    return partida

@app.get(
    "/jogadores",
    response_model=List[schemas.JogadorResponse],
    tags=["Jogadores"]
)
def listar_jogadores(
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    jogadores = db.query(models.Jogador).limit(limit).all()
    return jogadores