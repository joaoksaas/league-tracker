import requests


def get_puuid(game_name, tag_line, api_key):
    """
    Busca o PUUID do jogador usando o Riot ID (Nome #Tag).
    Utiliza a rota regional 'americas'.
    """
    
    # A Riot recomenda usar a rota 'americas' para buscar contas do BR
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    
    headers = {
        "X-Riot-Token": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        
        # Levanta exceção para erros de status (404, 401, 403, etc)
        response.raise_for_status() 
        
        data = response.json()
        return data.get('puuid')
    
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"Erro: Jogador {game_name}#{tag_line} não encontrado.")
        elif response.status_code == 403:
            print("Erro: API Key inválida ou expirada.")
        else:
            print(f"Erro HTTP: {err}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None
    


