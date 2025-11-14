from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TipoFila(int, Enum):
    CUSTOM = 0
    NORMAL_DRAFT = 400
    RANKED_SOLO = 420
    NORMAL_BLIND = 430
    RANKED_FLEX = 440
    ARAM = 450
    CLASH = 700
    ARAM_CLASH = 720
    INTRO_BOTS = 830
    BEGINNER_BOTS = 840
    INTERMEDIATE_BOTS = 850
    URF = 900
    ONE_FOR_ALL = 1020
    NEXUS_BLITZ = 1300
    ULTIMATE_SPELLBOOK = 1400

class Posicao(str, Enum):
    TOP = "TOP"
    JUNGLE = "JUNGLE"
    MIDDLE = "MIDDLE"
    BOTTOM = "BOTTOM"
    UTILITY = "UTILITY"

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        populate_by_name=True
    )

class JogadorBase(BaseSchema):
    nome_jogador: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Riot ID do jogador",
        examples=["Hide on bush", "Faker"]
    )

    icone_id: Optional[int] = Field(
        default=0,
        ge=0,
        description="ID do ícone de perfil"
    )

    nivel: Optional[int] = Field(
        default=1,
        ge=1,
        le=9999,
        description="Nível do invocador"
    )

class JogadorCreate(BaseSchema):
    nome_jogador: str = Field(
        ...,
        min_length=3,
        max_length=16,
        description="riot id do jogador",
        examples=["Hide on bush", "Keria"]
    )
    tag_line: str = Field(
        ...,
        min_length=3,
        max_length=5,
        description="tag do jogador (ex: BR1, NA1)"
    )

    @field_validator('nome_jogador')
    @classmethod
    def validate_nome(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("nome não pode ser vazio")
        return v.strip()

    @field_validator('tag_line')
    @classmethod
    def validate_tag(cls, v: str) -> str:
        tag = v.strip().upper()
        if not tag.isalnum():
            raise ValueError("tag deve conter apenas letras e números")
        return tag

class JogadorUpdate(BaseSchema):
    nome_jogador: Optional[str] = Field(None, min_length=1, max_length=100)
    icone_id: Optional[int] = Field(None, ge=0)
    nivel: Optional[int] = Field(None, ge=1, le=9999)

class JogadorResponse(JogadorBase):
    id: int
    puuid: str = Field(..., description="PUUID único do jogador")
    created_at: datetime
    updated_at: datetime

    total_partidas: Optional[int] = Field(None, description="total de partidas jogadas")
    total_vitorias: Optional[int] = Field(None, description="total de vitórias")
    winrate: Optional[float] = Field(None, ge=0.0, le=1.0, description="taxa de vitória (0.0-1.0)")

class JogadorDetalhado(JogadorResponse):
    participacoes: Optional[List['ParticipacaoResponse']] = Field(None, description="lista de participações em partidas")

class PartidaBase(BaseSchema):
    partida_id: str = Field(
        ...,
        pattern=r'^[A-Z]{2,4}1_\d+$',
        description="match id da riot"
    )
    data_partida: int = Field(
        ...,
        gt=0,
        description="timestamp da partida em millisegundos"
    )
    duracao_partida: int = Field(
        ...,
        gt=0,
        le=7200,
        description="duração em segundos"
    )
    tipo_fila: int = Field(
        ...,
        description="Queue ID (420=ranked solo, 440=flex, etc)"
    )
    patch: str = Field(
        ...,
        pattern=r'^\d+\.\d+',
        description="versão do jogo"
    )

class PartidaResponse(PartidaBase):
    id: int
    created_at: datetime
    participacao: Optional['ParticipacaoResponse'] = None

    duracao_formatada: Optional[str] = Field(None, description="duração formatada (MM:SS)")
    data_formatada: Optional[str] = Field(None, description="data formatada")

class PartidaDetalhada(PartidaResponse):
    participacoes: Optional[list['ParticipacaoResponse']] = Field(None, description="lista de participações (10 jogadores)")

class ParticipacaoBase(BaseSchema):
    campeao: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="nome do campeão"
    )

    abates: int = Field(default=0, ge=0, le=100)
    mortes: int = Field(default=0, ge=0, le=100)
    assistencias: int = Field(default=0, ge=0, le=100)
    cs: int = Field(default=0, ge=0, description="Creep Score")
    resultado: bool = Field(..., description="True=vitória, False=derrota")
    posicao: Optional[str] = Field(None, description="TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY")
    dano_campeoes: int = Field(default=0, ge=0)
    kda: float = Field(default=0.0, ge=0.0, le=100.0)
    pontuacao_visao: int = Field(default=0, ge=0)
    ouro_ganho: int = Field(default=0, ge=0)
    cs_jungle: int = Field(default=0, ge=0)
    penta_kills: int = Field(default=0, ge=0, le=10)
    quadra_kills: int = Field(default=0, ge=0, le=20)
    double_kills: int = Field(default=0, ge=0, le=50)
    fb_kill: bool = Field(default=False, description="First Blood Kill")
    fb_assist: bool = Field(default=False, description="First Blood Assist")

    @field_validator('posicao')
    @classmethod
    def validate_posicao(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == '':
            return None
        
        posicoes_validas = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY']
        v_upper = v.upper()

        mapa = {
            'MID': 'MIDDLE',
            'ADC': 'BOTTOM',
            'SUPPORT': 'UTILITY',
            'SUP': 'UTILITY',
            'BOT': 'BOTTOM'
        }

        v_upper = mapa.get(v_upper, v_upper)

        if v_upper not in posicoes_validas:
            raise ValueError(f"Posição inválida. Use: {', '.join(posicoes_validas)}")
        
        return v_upper
    
class ParticipacaoCreate(ParticipacaoBase):
    jogador_id: int = Field(..., gt=0)
    partida_id: int = Field(..., gt=0)

class ParticipacaoResponse(ParticipacaoBase):
    id: int
    jogador_id: int
    partida_id: int
    created_at: datetime

    kill_participation: Optional[int] = Field(None, description="abates + assistências")
    cs_total: Optional[int] = Field(None, description="cs total (lane + jungle)")
    cs_por_minuto: Optional[float] = Field(None, ge=0.0, description="cs por minuto")
    resultado_texto: Optional[str] = Field(None, description="'vitória' ou 'derrota'")

class ParticipacaoDetalhada(ParticipacaoResponse):
    jogador: Optional[JogadorResponse] = None
    partida: Optional[PartidaResponse] = None

class SincronizarPartidaRequest(BaseSchema):
    nome_jogador: Optional[str] = Field(None, description="nome do jogador")
    tag_line: Optional[str] = Field(None, description="tag do jogador")
    quantidade: int = Field(
        default=5,
        ge=1,
        le=100,
        description="quantidade de partidas a sincronizar"
    )
    apenas_ranked: bool = Field(
        default=False,
        description="sincronizar apenas ranked"
    )

class SincronizarPartidaResponse(BaseSchema):
    status: str = Field(..., description="status da operação")
    partidas_sincronizadas: int = Field(..., ge=0)
    partidas_duplicadas: int = Field(default=0, ge=0)
    erros: List[str] = Field(default_factory=list)
    tempo_execucao: Optional[float] = Field(None, description="tempo em segundos")

class EstatisticasJogador(BaseSchema):
    jogador_id: int
    nome_jogador: str
    total_partidas: int = Field(ge=0)
    total_vitorias: int = Field(ge=0)
    total_derrotas: int = Field(ge=0)
    winrate: float = Field(ge=0.0, le=1.0)
    
    kda_medio: float = Field(ge=0.0)
    abates_medio: float = Field(ge=0.0)
    mortes_medio: float = Field(ge=0.0)
    assistencias_medio: float = Field(ge=0.0)
    cs_medio: float = Field(ge=0.0)
    dano_medio: int = Field(ge=0)
    ouro_medio: int = Field(ge=0)

    top_campeoes: Optional[list[dict]] = Field(None, description="top 5 campeões mais jogados")
    posicoes: Optional[dict] = Field(None, description="distribuição por posição")

class HistoricoPartidas(BaseSchema):
    total: int = Field(ge=0, description="total de partidas")
    pagina: int = Field(ge=1, description="página atual")
    por_pagina: int = Field(ge=1, le=100, description="itens por página")
    partidas: List[PartidaDetalhada] = Field(default_factory=list)

class ErrorResponse(BaseSchema):
    error: str = Field(..., description="tipo do erro")
    message: str = Field(..., description="mensagem de erro")
    details: Optional[dict] = Field(None, description="detalhes adicionais")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SuccessResponse(BaseSchema):
    success: bool = Field(default=True)
    message: str
    data: Optional[dict] = None

class FiltroPartidas(BaseSchema):
    jogador_id: Optional[int] = Field(None, gt=0)
    tipo_fila: Optional[int] = None
    data_inicio: Optional[datetime] = Field(None, description="data inicial (inclusive)")
    data_fim: Optional[datetime] = Field(None, description="data final (inclusive)")
    apenas_vitorias: Optional[bool] = None
    campeao: Optional[str] = None
    posicao: Optional[str] = None

    pagina: int = Field(default=1, ge=1)
    por_pagina: int = Field(default=20, ge=1, le=100)

    ordenar_por: str = Field(default="data_partida", description="campo para ordenação")
    ordem_desc: bool = Field(default=True, description="ordem decrescente")

    @field_validator('data_fim')
    @classmethod
    def validate_datas(cls, v, info):
        data_inicio = info.data.get('data_inicio')
        if v and data_inicio and v < data_inicio:
            raise ValueError("data_fim deve ser maior ou igual a data_inicio")
        return v

class FiltroEstatisticas(BaseSchema):
    jogador_id: int = Field(..., gt=0)
    tipo_fila: Optional[int] = None
    campeao: Optional[str] = None
    posicao: Optional[str] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    temporada: Optional[int] = Field(None, ge=2009, description="ano da temporada")

JogadorDetalhado.model_rebuild()
PartidaDetalhada.model_rebuild()
ParticipacaoDetalhada.model_rebuild()
PartidaResponse.model_rebuild()  