# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# %%
engine = create_engine('sqlite:///lol_matches.db')

# %%
query = 'SELECT * FROM tb_match_stats'

df = pd.read_sql(query, con=engine)
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
