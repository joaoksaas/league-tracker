import os
import json
import time
import requests
from dotenv import load_dotenv
from puuid import get_puuid

load_dotenv()
API_KEY = os.getenv('RIOT_API_KEY')
HEADERS = {"X-Riot-Token": API_KEY} 
BASE_PATH = "match_history" # Pasta raiz dos dados



# --- EXTRAÇÃO ---
def fetch_and_save_matches(nick, puuid, count):
    # 1. Busca a lista de IDs primeiro (evita criar pasta se a API falhar)
    url_ids = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    response = requests.get(url_ids, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Erro ao buscar IDs (Status {response.status_code}). Verifique sua API Key!")
        return
    

    match_ids = response.json()
    print(f"Partidas encontradas para {nick}: {len(match_ids)}")

    if not match_ids:
        print("Nenhuma partida recente encontrada para este jogador nesta região.")
        return

    # 2. Cria a pasta apenas se houver partidas para baixar
    player_folder = os.path.join(BASE_PATH, nick)
    os.makedirs(player_folder, exist_ok=True)

    # 3. Loop de download
    for m_id in match_ids:
        file_path = os.path.join(player_folder, f"{m_id}.json")
        
        if not os.path.exists(file_path):
            print(f"Baixando partida {m_id} para o perfil [{nick}]...")
            url_detail = f"https://americas.api.riotgames.com/lol/match/v5/matches/{m_id}"
            res = requests.get(url_detail, headers=HEADERS)
            
            if res.status_code == 200:
                with open(file_path, 'w') as f:
                    json.dump(res.json(), f)
                time.sleep(1.2) # Rate Limit - 20 requests a cada 1 segundo / 100 requests a cada 2 minutos
            else:
                print(f"Erro no download da partida {m_id}: {res.status_code}")
        else:
            print(f"Partida {m_id} já está no cache. Pulando...")

    print("Todos as partidas foram baixadas com sucesso!")


# --- EXECUÇÃO ---
nick = os.getenv('NICK')
riot_id = os.getenv('RIOT_ID')

puuid_alvo = get_puuid(nick, riot_id, API_KEY) # Nick, RiotID (sem o #), API_KEY

# O bloco condicional agora protege a execução corretamente
if puuid_alvo:
    print("PUUID capturado!") 
    print(f"Iniciando extração para {puuid_alvo}...")
    fetch_and_save_matches("player1", puuid_alvo, 20) # nome da pasta, puuid desejado, número de partidas para download
else:
    print("Debug: Erro! O PUUID não foi encontrado. Verifique o Nick e a Tag.")