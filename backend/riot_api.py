# esse arquivo terá a "preocupação" de conversar com a API da Riot. Ela é uma "especialista" em buscar dados externos.
# importar modulos
import requests

# variaveis globais
API_KEY = 'RGAPI-7b3819e6-1c3f-4b32-a2d1-376ccfd78923' # chave api
tag_line = '7585' # tag line do jogador
nome_jogador = 'tequila sunset' # nome do jogador

# função retornar uma string com o valor do puuid do jogador
def get_puuid(nome_jogador: str, tag_line: str, API_KEY: str) -> str:
    return requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nome_jogador}/{tag_line}?api_key={API_KEY}").json().get('puuid')

# função para retornar uma lista com os id de cada partida do histórico
def get_partidas_id(puuid: str, API_KEY: str, count: int) -> list:
    return requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={API_KEY}&count={count}").json()

# função para retornar uma lista com as informações da partida
def get_partida_info(matchId: str, API_KEY: str) -> list:
    return requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={API_KEY}").json()

# função para retornar uma lista com os participantes da partida
def get_lista_participantes(matchId: str) -> list:
    return requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={API_KEY}").json().get('metadata').get('participants')

# função para retornar os dados do jogador na partida
def get_jogador_dados(lista_participantes: list, jogador_puuid: str, matchId: str) -> list:
    # encontrar o index do jogador na lista de participantes da partida 
    for index, puuid in enumerate(lista_participantes):
        if puuid == jogador_puuid:
            index_jogador = index
    
    #puxar os dados da partidas
    dados_partida = get_partida_info(matchId, API_KEY)

    # armazenar cada dado do jogador da partida em sua respectivel variavel
    campeao = dados_partida['info']['participants'][index_jogador]['championName']
    abates = dados_partida['info']['participants'][index_jogador]['kills']
    mortes = dados_partida['info']['participants'][index_jogador]['deaths']
    assistencias = dados_partida['info']['participants'][index_jogador]['assists']
    cs = dados_partida['info']['participants'][index_jogador]['totalMinionsKilled']

    return {'campeao': campeao, 'abates': abates, 'mortes': mortes, 'assistencias': assistencias, 'cs': cs}