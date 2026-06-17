# %%
import os
import json
import pandas as pd
from dotenv import load_dotenv
from puuid import get_puuid
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
# %%

engine = create_engine('sqlite:///lol_matches.db')

# --- TRANSFORMA EM DATAFRAME ---
def analyze_local_data(my_puuid, nick):
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

load_dotenv()

nome = os.getenv('NOME') 
tag = os.getenv('TAG')
API_KEY = os.getenv('RIOT_API_KEY')

puuid = get_puuid(nome, tag, API_KEY)

player = "saas" # nome para identificação do jogador nas tabelas e arquivos

df = analyze_local_data(puuid, player)

# %%
# --- CONEXÃO SQL ---

if not df.empty:

    df['items'] = df['items'].apply(lambda x: ','.join(map(str, x))) # o SQLite não entende listas, essa linha transforma a lista de itens em uma string

    df['player_name'] = player # atribui a linha a um jogador, no caso de haverem mais jogadores a serem analizados

    df.to_sql(
        name='tb_match_stats',   # Nome da tabela que será criada
        con=engine,              
        if_exists='append',      # Se a tabela já existir, adiciona os dados no final
        index=False              # Não salva o índice do Pandas como uma coluna
    )
    print(f"Dados do jogador [{player}] unificados com sucesso!")
else:
    print("Nenhum dado encontrado para salvar.")


# --- ANÁLISES ---

# %%
ranked = df[df["game_mode"] == "CLASSIC"]
demais_modos = df[df["game_mode"] != "CLASSIC"]
# %%
win_rate_ranked = ranked["win"].mean()
win_rate_ranked*100
# %%
stats_on_win_ranked = ranked.groupby("win")[["gold_per_min", "kda", "damage_dealt", "vision_score"]].mean().T # .t é de Transpose, gira a tebela
stats_on_win_ranked

#fb_on_win_ranked = ranked.groupby("win")["first_blood"].agg(lambda x: x.mode()[0])
#fb_on_win_ranked

# %%

analise_performance = ranked.groupby("win")[["gold_per_min", "kda", "damage_dealt", "vision_score"]].mean().T
analise_performance.columns = ["Derrota", "Vitória"]

# Criando uma coluna de 'Upgrade' para ver quanto você melhora quando ganha
analise_performance["Diferença (%)"] = (analise_performance["Vitória"] / analise_performance["Derrota"] - 1) * 100

print(analise_performance)

# %%
# 1. Seleciona apenas as colunas de métricas que fazem sentido cruzar
colunas_analise = ["win", "gold_per_min", "kda", "damage_dealt", "vision_score", "time_ccing", "first_blood"]

# 2. Calcula a matriz de correlação (usando o método de Pearson por padrão)
matriz_corr = ranked[colunas_analise].corr()

# 3. Exibe a correlação especificamente com a VITÓRIA, ordenada do maior para o menor
print("--- O que mais se correlaciona com a sua Vitória ---")
print(matriz_corr["win"].sort_values(ascending=False))

# %%
# Gráfico de correlação
plt.figure(figsize=(10, 8))

# Cria o heatmap
sns.heatmap(
    matriz_corr, 
    annot=True,          # Coloca os números dentro dos quadradinhos
    cmap="coolwarm",     # Paleta de cores (Azul para negativo, Vermelho para positivo)
    fmt=".2f",           # Limita para duas casas decimais
    vmin=-1, vmax=1      # Força a escala a ir de -1 a 1
)

plt.title("Matriz de Correlação - Performance no LoL")
plt.show()
# %%
