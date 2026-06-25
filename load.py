import os
import json
import pandas as pd
from dotenv import load_dotenv
from puuid import get_puuid
from sqlalchemy import create_engine, inspect

# --- TRANSFORMA EM DATAFRAME ---
def load_local_data(my_puuid, nick):
    path = f"match_history/{nick}"
    all_stats = []

    for file in os.listdir(path):
        if file.endswith(".json"):
            with open(f"{path}/{file}", 'r') as f:
                data = json.load(f)
                
                # Procura o player entre os participantes
                participants = data['info']['participants']
                me = next((p for p in participants if p['puuid'] == my_puuid), None) # o PUUID é necessário aqui, para identificar o player nas partidas
                
                if me:
                    all_stats.append({
                        'match_id': file.replace('.json', ''),
                        'date': data['info']['gameCreation'],
                        'champion': me['championName'],
                        'win': me['win'],
                        'game_mode': data['info']['gameMode'],      # Ex: CLASSIC, ARAM, CHERRY (Arena)
                        'game_type': data['info']['gameType'],      # Ex: MATCHED_GAME
                        'queue_id': data['info']['queueId'],        # ID da fila (SoloQ ou Flex)
                        'kda': (me['kills'] + me['assists']) / max(1, me['deaths']),
                        'gold_per_min': me['goldEarned'] / (data['info']['gameDuration'] / 60),
                        'items': [me[f'item{i}'] for i in range(7)],
                        
                        # Extras interessantes que a API oferece:
                        'damage_dealt': me['totalDamageDealtToChampions'],          # Dano Causado
                        'vision_score': me['visionScore'],          # Placar de Visão
                        'time_ccing': me['timeCCingOthers'],        # Controle de Grupo
                        'first_blood': me['firstBloodKill']         # Primeira morte
                    })  


    df = pd.DataFrame(all_stats)
    # Converter timestamp para data legível
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    return df


# --- EXECUÇÃO ---
def load_to_db(df, player, engine):
    if not df.empty:

        df['items'] = df['items'].apply(lambda x: ','.join(map(str, x))) # o SQLite não entende listas, essa linha transforma a lista de itens em uma string

        df['player_name'] = player # atribui a linha a um jogador, no caso de haverem mais jogadores a serem analizados

        if inspect(engine).has_table('tb_match_stats'):
            partidas_no_banco = pd.read_sql('SELECT match_id FROM tb_match_stats', con=engine) # seleciona todas as partidas presentes no banco
            ids_existentes = partidas_no_banco['match_id'].tolist() # pega os IDs dessas partidas selecionadas

            df_filtrado = df[~df['match_id'].isin(ids_existentes)] # verifica quais partidas do df atual estão presentes no banco
        else:
            df_filtrado = df

        if not df_filtrado.empty:
            df_filtrado.to_sql(
                name='tb_match_stats',   # Nome da tabela que será criada
                con=engine,              
                if_exists='append',      # Se a tabela já existir, adiciona os dados no final
                index=False              # Não salva o índice do Pandas como uma coluna
            )
            print(f"Dados do jogador [{player}] unificados com sucesso!")
            print(f"{len(df_filtrado)} partidas novas adicionadas!")
        else:
            print("Todas as partidas analisadas já existem no banco de dados. Nada foi inserido.")

    else:
        print("Nenhum dado encontrado para processar.")


engine = create_engine('sqlite:///lol_matches.db')

load_dotenv()

nome = os.getenv('NOME') 
tag = os.getenv('TAG')
API_KEY = os.getenv('RIOT_API_KEY')
player = "saas" # nome para identificação do jogador nas tabelas e arquivos, em caso de mais de 1 conta por jogador

puuid = get_puuid(nome, tag, API_KEY)

df = load_local_data(puuid, player)

load_to_db(df, player, engine)




