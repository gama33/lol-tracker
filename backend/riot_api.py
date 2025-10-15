# esse arquivo terá a "preocupação" de conversar com a API da Riot. Ela é uma "especialista" em buscar dados externos.
# importar modulo requests
import requests

#chave da API riot
API_KEY = 'RGAPI-6e62aacf-c71c-47a4-a87e-11c84879b14e'

# variaveis globais
tag_line = '7585'
game_name = 'tequila sunset'

# função para buscar o puuid do jogador
def get_puuid(summoner_name: str, tag_line: str, API_KEY: str) -> str:
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}?api_key={API_KEY}"
    return requests.get(url).json().get('puuid')

# salvar o puuid em uma variavel
puuid = get_puuid(game_name, tag_line, API_KEY)

#função para buscar os ids das partidas do jogador
def get_partidas_ids(puuid: str, API_KEY: str, count: int = 20) -> list:
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={API_KEY}&count={count}"
    return requests.get(url).json()