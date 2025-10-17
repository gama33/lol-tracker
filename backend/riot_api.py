# esse arquivo terá a "preocupação" de conversar com a API da Riot. Ela é uma "especialista" em buscar dados externos.
# importar modulo requests
import requests

#chave da API riot
API_KEY = 'RGAPI-7b3819e6-1c3f-4b32-a2d1-376ccfd78923'

# variaveis globais
tag_line = '7585'
game_name = 'tequila sunset'

# função para buscar o puuid do jogador
def get_puuid(summoner_name: str, tag_line: str, API_KEY: str) -> str:
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}?api_key={API_KEY}"
    return requests.get(url).json().get('puuid')

# salvar o puuid em uma variavel
puuid = get_puuid(game_name, tag_line, API_KEY)

#função para buscar os ids das partidas do jogador ("historico de partidas")
def get_historico_partidas_ids(puuid: str, API_KEY: str, count: int = 5) -> list:
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={API_KEY}&count={count}"
    return requests.get(url).json()

# função para retornar todos as informações de cada partida do histórico
def get_dados_da_partida(matchId: str, API_KEY: str):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={API_KEY}"
    return requests.get(url).json()

# função para receber as informações da partida pelo id das partidas do histórico e sincronizar com o banco de dados
def sincronizar_e_salvar_partidas():
    lista_de_ids = get_historico_partidas_ids()
    for id in lista_de_ids:
        detalhes_partida = get_dados_da_partida(id, API_KEY)





