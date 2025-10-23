# esse arquivo terá a "preocupação" de conversar com a API da Riot. Ela é uma "especialista" em buscar dados externos.
# importar modulos
import requests
import os

# variaveis globais
API_KEY = os.environ.get('RIOT_API_KEY') # chave api importado do ambiente de variaveis global
nome_jogador = 'tequila sunset' # nome do jogador
tag_line = '7585' # tag line do jogador

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
            break # para o loop assim que encontrar 
    
    #puxar os dados da partidas e salvar o dicionario em uma varaivel
    dados_partida = get_partida_info(matchId, API_KEY)
    dados_partida_info = dados_partida['info']
    dados_partida_jogador = dados_partida_info['participants'][index_jogador]

    # armazenar cada dado do jogador da partida em sua respectivel variavel
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
    kda = dados_partida_jogador.get('challenges', {}).get('kda', 0.0) # .get() para evitar erro se 'challenges' não existir
    pontuacao_visao = dados_partida_jogador['visionScore'] 
    ouro_ganho = dados_partida_jogador['goldEarned']
    cs_jungle = dados_partida_jogador['neutralMinionsKilled']
    penta_kills = dados_partida_jogador['pentaKills']
    quadra_kills = dados_partida_jogador['quadraKills']
    double_kills = dados_partida_jogador['doubleKills']
    fb_kill = dados_partida_jogador['firstBloodKill']
    fb_assist = dados_partida_jogador['firstBloodAssist']

    # armazenar cada dado da partida em sua respectivel variavel
    data_partida = dados_partida_info['gameCreation']
    duracao_partida = dados_partida_info['gameDuration']
    tipo_fila = dados_partida_info['queueId']
    patch = dados_partida_info['gameVersion']

    #retorna as valores para popular o banco de dados
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