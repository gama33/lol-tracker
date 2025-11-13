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

class Regiao(str, Enum):
    AMERICAS = "americas"
    ASIA = "asia"
    EUROPE = "europe"
    SEA = "sea"

class Plataforma(str, Enum):
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

class RateLimitException(RiotAPIException):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limit excedido. Tente novamente em {retry_after} segundos", status_code=429)

class NotFoundException(RiotAPIException):
    def __init__(self, resource: str):
        super().__init__(f"Recurso não encontrado: {resource}", status_code=404)

class UnauthorizedException(RiotAPIException):
    def __init__(self):
        super().__init__("API Key inválida, expirada ou bloqueada", status_code=403)

class SimpleRateLimiter:
    def __init__(self, max_calls: int, period: int):
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def esperar_se_necessario(self):
        now = time.time()

        self.calls = [call_time for call_time in self.calls
                      if now - call_time < self.period]
        
        if len(self.calls) >= self.max_calls:
            sleep_time = self.period - (now - self.calls[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                self.calls = []

        self.calls.append(time.time())

rate_limiter_second = SimpleRateLimiter(APP_RATE_LIMIT_PER_SECOND, 1)
rate_limiter_2min = SimpleRateLimiter(APP_RATE_LIMIT_PER_2MIN, 120)

def _make_request(url: str, timeout: int = REQUEST_TIMEOUT, retry_count: int = 0) -> Dict:
    rate_limiter_second.esperar_se_necessario()
    rate_limiter_2min.esperar_se_necessario()

    try:
        response = requests.get(url, timeout=timeout)

        if response.status_code == 200:
            return response.json()
        
        if response.status_code == 404:
            raise NotFoundException(url)
        
        elif response.status_code == 401:
            raise RiotAPIException("API key não fornecida", status_code=401)
        
        elif response.status_code == 403:
            raise UnauthorizedException()
        
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 1))
            raise RateLimitException(retry_after)
        
        elif response.status_code == 400:
            raise RiotAPIException("Requisição inválida - verifique os parâmetros", status_code=400)

        elif response.status_code >= 500:
            if retry_count < MAX_ENTRIES:
                wait_time = RETRY_DELAY * (2 ** retry_count)
                time.sleep(wait_time)
                return _make_request(url, timeout, retry_count + 1)
            else:
                raise RiotAPIException(f"Erro no servidor da Riot (tentou {MAX_ENTRIES} vezes)", status_code=response.status_code)

        else:
            raise RiotAPIException(f"Erro HTTP {response.status_code}: {response.text}", status_code=response.status_code)

    except Timeout:
        if retry_count < MAX_ENTRIES:
            wait_time = RETRY_DELAY * (2 ** retry_count)
            time.sleep(wait_time)
            return _make_request(url, timeout, retry_count + 1)
        else:
            raise RiotAPIException(f"Timeout após {MAX_ENTRIES} tentativas: {url}")
        
    except RiotAPIException:
        raise

    except RequestException as e:
        raise RiotAPIException(f"Erro na requisição: {str(e)}")
    
def _build_url(endpoint: str, region: str = "americas", **params) -> str:
    base_url = f"https://{region}.api.riotgames.com"

    if 'api_key' not in params:
        params['api_key'] = API_KEY

    query_string = '&'.join([f"{k}={v}" for k, v in params.items() if v is not None])

    return f"{base_url}{endpoint}?{query_string}"

def get_puuid(nome_jogador: str, tag_line: str, api_key: Optional[str] = None, region: str = 'americas') -> str:
    api_key = api_key or API_KEY
    if not api_key:
        raise RiotAPIException("API Key não configurada")
    
    from urllib.parse import quote
    nome_encoded = quote(nome_jogador)
    url = _build_url(f"/riot/account/v1/accounts/by-riot-id/{nome_encoded}/{tag_line}", region=region, api_key=api_key)
    data = _make_request(url)
    puuid = data.get('puuid')
    if not puuid:
        raise RiotAPIException(f"PUUID não encontrado na resposta para {nome_jogador}#{tag_line}")
        
    return puuid

def get_partidas_id(puuid: str, count: int = 20, start: int = 0, queue: Optional[int] = None, type: Optional[str] = None, api_key: Optional[str] = None, region: str = 'americas') -> List[str]:
    api_key = api_key or API_KEY
    if not api_key:
        raise RiotAPIException('API Key não configurada')

    if count < 0:
        count = 20
    elif count > 100:
        count = 100

    params = {
        'api_key': api_key,
        'count': count,
        'start': start
    }

    if queue is not None:
        params['queue'] = queue
    if type is not None:
        params['type'] = type

    url = _build_url(f"/lol/match/v5/matches/by-puuid/{puuid}/ids", region=region, **params)

    matches = _make_request(url)

    if not isinstance(matches, list):
        raise RiotAPIException("Resposta inesperada da API: esperava lista de partidas")

    return matches

def get_partida_info(match_id: str, api_key: Optional[str] = None, region: str = 'americas') -> Dict:
    api_key = api_key or API_KEY
    if not api_key:
        raise RiotAPIException('API Key não configurada')

    url = _build_url( f"/lol/match/v5/matches/{match_id}", region=region, api_key=api_key)
    data = _make_request(url)

    if 'metadata' not in data or 'info' not in data:
        raise RiotAPIException(f"Resposta da API incompleta para partida {match_id}")
    
    return data
    
def get_lista_participantes(match_id: str, api_key: Optional[str] = None, region: str = 'americas') -> List[str]:
    data = get_partida_info(match_id, api_key, region)
    
    participantes = data.get('metadata', {}).get('participants', [])
    
    if not participantes:
        raise RiotAPIException(
            f"Lista de participantes vazia para partida {match_id}"
        )
    
    if len(participantes) != 10:
        raise RiotAPIException(
            f"Número incorreto de participantes: esperado 10, recebido {len(participantes)}"
        )
    
    return participantes

def get_dados_partida(match_id: str, api_key: Optional[str] = None, region: str = 'americas') -> Dict[str, Any]:
    data = get_partida_info(match_id, api_key, region)
    info = data.get('info', {})

    if not info:
        raise RiotAPIException(f"Informações da partida {match_id} não encontradas")

    return {
        'partida_id': match_id,
        'data_partida': info.get('gameCreation', 0),
        'duracao_partida': info.get('gameDuration', 0),
        'tipo_fila': info.get('queueId', 0),
        'patch': info.get('gameVersion', 'unknown'),
    }

def get_dados_participacao(match_id: str, jogador_puuid: str, api_key: Optional[str] = None, region: str = 'americas') -> Dict[str, Any]:
    
    data = get_partida_info(match_id, api_key, region)
    participantes = data.get('info', {}).get('participants', [])
    jogador_data = None
    
    for participante in participantes:
        if participante.get('puuid') == jogador_puuid:
            jogador_data = participante
            break

    if not jogador_data:
        raise RiotAPIException(f"Jogador {jogador_puuid} não encontrado na partida {match_id}")

    return {
        'campeao': jogador_data.get('championName', 'Unknown'),
        'abates': jogador_data.get('kills', 0),
        'mortes': jogador_data.get('deaths', 0),
        'assistencias': jogador_data.get('assists', 0),
        'cs': jogador_data.get('totalMinionsKilled', 0),
        'resultado': jogador_data.get('win', False),  # Boolean!
        'posicao': jogador_data.get('teamPosition', ''),
        'dano_campeoes': jogador_data.get('totalDamageDealtToChampions', 0),
        'kda': jogador_data.get('challenges', {}).get('kda', 0.0),
        'pontuacao_visao': jogador_data.get('visionScore', 0),
        'ouro_ganho': jogador_data.get('goldEarned', 0),
        'cs_jungle': jogador_data.get('neutralMinionsKilled', 0),
        'penta_kills': jogador_data.get('pentaKills', 0),
        'quadra_kills': jogador_data.get('quadraKills', 0),
        'double_kills': jogador_data.get('doubleKills', 0),
        'fb_kill': jogador_data.get('firstBloodKill', False),
        'fb_assist': jogador_data.get('firstBloodAssist', False)
    }

def get_dados_completos_partida(match_id: str, api_key: str, region: str = 'americas') -> Dict[str, Any]:
    data = get_partida_info(match_id, api_key, region)
    info = data['info']

    partida = {
        'partida_id': match_id,
        'data_partida': info.get('gameCreation', 0),
        'duracao_partida': info.get('gameDuration', 0),
        'tipo_fila': info.get('queueId', 0),
        'patch': info.get('gameVersion', 'unknown')
    }

    participacoes = []
    for participante in info.get('participants', []):
        participacoes.append({
            'puuid': participante.get('puuid'),
            'campeao': participante.get('championName', 'Unknown'),
            'abates': participante.get('kills', 0),
            'mortes': participante.get('deaths', 0),
            'assistencias': participante.get('assists', 0),
            'cs': participante.get('totalMinionsKilled', 0),
            'resultado': participante.get('win', False),
            'posicao': participante.get('teamPosition', ''),
            'dano_campeoes': participante.get('totalDamageDealtToChampions', 0),
            'kda': participante.get('challenges', {}).get('kda', 0.0),
            'pontuacao_visao': participante.get('visionScore', 0),
            'ouro_ganho': participante.get('goldEarned', 0),
            'cs_jungle': participante.get('neutralMinionsKilled', 0),
            'penta_kills': participante.get('pentaKills', 0),
            'quadra_kills': participante.get('quadraKills', 0),
            'double_kills': participante.get('doubleKills', 0),
            'fb_kill': participante.get('firstBloodKill', False),
            'fb_assist': participante.get('firstBloodAssist', False)
        })
    
    return {
        'partida': partida,
        'participacoes': participacoes
    }

def get_dados_summoner(puuid: str, api_key: Optional[str] = None, plataforma: str ='br1') -> Dict[str, Any]:
    api_key = api_key or API_KEY
    if not api_key:
        raise RiotAPIException('API key não configurada')
    
    url = f"https://{plataforma}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"

    data = _make_request(url)

    if not data:
        raise RiotAPIException(f"Dados do summoner não encontrados para PUUID {puuid}")
    
    return {
        'icone_id': data.get('profileIconId', 0),
        'nivel': data.get('summonerLevel', 1),
        'summoner_id': data.get('id', ''),
    }