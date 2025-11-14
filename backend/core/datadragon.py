import requests
import os
from datetime import datetime, timedelta

# --- Cache para a versão e dados dos campeões ---
CACHE_EXPIRATION = timedelta(hours=6)
_latest_version = None
_version_timestamp = None
_champion_data = None
_champion_timestamp = None

DDRAGON_BASE_URL = "http://ddragon.leagueoflegends.com"

def get_latest_version():
    """
    Busca a última versão do Data Dragon, com cache de 6 horas.
    """
    global _latest_version, _version_timestamp
    now = datetime.now()

    if _latest_version and _version_timestamp and (now - _version_timestamp < CACHE_EXPIRATION):
        return _latest_version

    try:
        response = requests.get(f"{DDRAGON_BASE_URL}/api/versions.json")
        response.raise_for_status()
        _latest_version = response.json()[0]
        _version_timestamp = now
        print(f"Nova versão do Data Dragon carregada: {_latest_version}")
        return _latest_version
    except requests.RequestException as e:
        print(f"Erro ao buscar versões do Data Dragon: {e}")
        # Retorna uma versão padrão em caso de falha
        return os.getenv("DDRAGON_FALLBACK_VERSION", "14.1.1")

def get_champion_data():
    """
    Busca os dados de todos os campeões, com cache de 6 horas.
    """
    global _champion_data, _champion_timestamp
    now = datetime.now()

    if _champion_data and _champion_timestamp and (now - _champion_timestamp < CACHE_EXPIRATION):
        return _champion_data

    version = get_latest_version()
    try:
        response = requests.get(f"{DDRAGON_BASE_URL}/cdn/{version}/data/en_US/champion.json")
        response.raise_for_status()
        _champion_data = response.json()['data']
        _champion_timestamp = now
        print("Dados dos campeões carregados.")
        return _champion_data
    except requests.RequestException as e:
        print(f"Erro ao buscar dados dos campeões: {e}")
        return None

def get_champion_icon_url(champion_name: str) -> str | None:
    """
    Retorna a URL do ícone de um campeão a partir do seu nome.
    """
    if not champion_name:
        return None

    champion_data = get_champion_data()
    if not champion_data:
        return None

    # O nome do campeão nos dados da API de partida às vezes é diferente do nome no Data Dragon
    # Ex: "Wukong" é "MonkeyKing". O campo 'key' no champion.json é o ID numérico, 'id' é o nome textual.
    # Precisamos encontrar o campeão pelo 'name' e usar o 'id' para a URL.
    
    formatted_champion_name = champion_name.replace(" ", "")
    
    champion_info = None
    for champ_id, champ_details in champion_data.items():
        if champ_details['name'].lower() == champion_name.lower() or champ_id.lower() == formatted_champion_name.lower():
            champion_info = champ_details
            break
    
    if champion_info:
        version = get_latest_version()
        champion_id = champion_info['id']
        return f"{DDRAGON_BASE_URL}/cdn/{version}/img/champion/{champion_id}.png"

    print(f"Ícone para o campeão '{champion_name}' não encontrado.")
    return None

# Pré-carregar os dados na inicialização do módulo
get_latest_version()
get_champion_data()
