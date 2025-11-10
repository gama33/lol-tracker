import requests
import os
import time
from typing import Dict, List, Optional, Any
from requests.exceptions import RequestException, HTTPError, Timeout
from datetime import datetime, timedelta
from enum import Enum

API_KEY = os.environ.get('RIOT_API_KEY')
RIOT_API_BASE_URL = "https://americas.api.riotgames.com"
REQUEST_TIMEOUT = 10
MAX_ENTRIES = 3
RETRY_DELAY = 1

APP_RATE_LIMIT_PER_SECOND = 20
APP_RATE_LIMIT_PER_2MIN = 100

nome_jogador = 'tequila sunset'
tag_line = '7585'

class Region(str, Enum):
    AMERICAS = "americas"
    ASIA = "asia"
    EUROPE = "europe"
    SEA = "sea"

class Plataform(str, Enum):
    BR1 = "br1"
    EUN1 = "eun1"
    EUW1 = "euw1"
    JP1 = "jp1"
    KR = "kr"
    LA1 = "la1"
    LA2 = "la2"
    NA1 = "na1"
    OC1 = "oc1"
    TR1 = "tr1"
    RU = "ru"
    PH2 = "ph2"
    SG2 = "sg2"
    TH2 = "th2"
    TW2 = "tw2"
    VN2 = "vn2"

class RiotAPIException(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)





def get_puuid(nome_jogador: str, tag_line: str, API_KEY: str) -> str:
    return requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nome_jogador}/{tag_line}?api_key={API_KEY}").json().get('puuid')

def get_partidas_id(puuid: str, API_KEY: str, count: int) -> list:
    return requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={API_KEY}&count={count}").json()

def get_partida_info(matchId: str, API_KEY: str) -> list:
    return requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={API_KEY}").json()

def get_lista_participantes(matchId: str) -> list:
    return requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={API_KEY}").json().get('metadata').get('participants')

def get_jogador_dados(lista_participantes: list, jogador_puuid: str, matchId: str) -> list:
    
    for index, puuid in enumerate(lista_participantes):
        if puuid == jogador_puuid:
            index_jogador = index
            break
    
    dados_partida = get_partida_info(matchId, API_KEY)
    dados_partida_info = dados_partida['info']
    dados_partida_jogador = dados_partida_info['participants'][index_jogador]

    partida_id = matchId
    campeao = dados_partida_jogador['championName']
    abates = dados_partida_jogador['kills']
    mortes = dados_partida_jogador['deaths']
    assistencias = dados_partida_jogador['assists']
    cs = dados_partida_jogador['totalMinionsKilled']
    resultado_boolean = dados_partida_jogador['win']
    resultado = 'Vitória' if resultado_boolean else 'Derrota'
    posicao = dados_partida_jogador['teamPosition']
    dano_campeoes = dados_partida_jogador['totalDamageDealtToChampions']
    kda = dados_partida_jogador.get('challenges', {}).get('kda', 0.0) 
    pontuacao_visao = dados_partida_jogador['visionScore'] 
    ouro_ganho = dados_partida_jogador['goldEarned']
    cs_jungle = dados_partida_jogador['neutralMinionsKilled']
    penta_kills = dados_partida_jogador['pentaKills']
    quadra_kills = dados_partida_jogador['quadraKills']
    double_kills = dados_partida_jogador['doubleKills']
    fb_kill = dados_partida_jogador['firstBloodKill']
    fb_assist = dados_partida_jogador['firstBloodAssist']
    data_partida = dados_partida_info['gameCreation']
    duracao_partida = dados_partida_info['gameDuration']
    tipo_fila = dados_partida_info['queueId']
    patch = dados_partida_info['gameVersion']
    return {
        'partida_id': partida_id,
        'campeao': campeao, 
        'abates': abates, 
        'mortes': mortes, 
        'assistencias': assistencias, 
        'cs': cs,
        'resultado': resultado,
        'data_partida': data_partida,
        'duracao_partida': duracao_partida,
        'tipo_fila': tipo_fila,
        'patch': patch,
        'posicao': posicao,
        'dano_campeoes': dano_campeoes,
        'kda': kda,
        'pontuacao_visao': pontuacao_visao,
        'ouro_ganho': ouro_ganho,
        'cs_jungle': cs_jungle,
        'penta_kills': penta_kills,
        'quadra_kills': quadra_kills,
        'double_kills': double_kills,
        'fb_kill': fb_kill,
        'fb_assist': fb_assist
    }