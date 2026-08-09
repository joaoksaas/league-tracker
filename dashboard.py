import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Lol Tracker", layout="wide")
st.title("Lol Tracker - Dashboard de Performance")

engine = create_engine('sqlite:///lol_matches.db')

@st.cache_data
def load_data():
    query = "SELECT * FROM tb_match_stats"
    df = pd.read_sql(query, con=engine)
    return df

df = load_data()

# --- Filtros ---
st.sidebar.header("Filtros")

# Jogador
player_list = df['player_name'].unique()
selected_player = st.sidebar.selectbox("Selecione o jogador", player_list)

# Champion
champion_list = ["Todos"] + list(df[df["player_name"] == selected_player]["champion"].unique())
selected_champion = st.sidebar.selectbox("Selecione o Campeão", champion_list)

# Tipo de Jogo
mode_list = ["Todos"] + list(df[df["player_name"] == selected_player]["game_mode"].unique())
selected_mode = st.sidebar.selectbox("Selecione o Modo de Jogo", mode_list)

df_filtrado = df[df["player_name"] == selected_player]
if selected_champion != "Todos":
    df_filtrado = df_filtrado[df_filtrado["champion"] == selected_champion]
if selected_mode != "Todos":
    df_filtrado = df_filtrado[df_filtrado["game_mode"] == selected_mode]

# --- Métricas ---
total_matches = len(df_filtrado)
winrate = (df_filtrado["win"].sum() / total_matches * 100) if total_matches > 0 else 0
kda_medio = df_filtrado["kda"].mean() if total_matches > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total de Partidas", total_matches)
col2.metric("Winrate (%)", f"{winrate:.2f}")
col3.metric("KDA Médio", f"{kda_medio:.2f}")

st.markdown("---")

# --- Gráficos ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Gold por Minuto")

    fig_gold = px.line(df_filtrado.sort_values('date'), x='date', y='gold_per_min', title="Gold por Minuto ao Longo da Partida", markers=True)

    st.plotly_chart(fig_gold, use_container_width=True)

with col_graf2:
    st.subheader("Distribuição de Vitórias e Derrotas")
    
    df_pizza = df_filtrado.copy()
    
    df_pizza['resultado'] = df_pizza['win'].astype(str).map({
        '1': 'Vitória', 'True': 'Vitória',
        '0': 'Derrota', 'False': 'Derrota'
    })
    
    df_win_count = df_pizza['resultado'].value_counts().reset_index()
    
    if not df_win_count.empty:
        fig_pizza = px.pie(
            df_win_count, 
            names='resultado',   # Nome ajustado para a nova coluna
            values='count', 
            hole=0.4,
            color='resultado', 
            color_discrete_map={'Vitória': '#2ca02c', 'Derrota': '#d62728'}
        )
        
        #fig_pizza.update_layout(showlegend=False)
        
        st.plotly_chart(fig_pizza, use_container_width=True)
    else:
        st.warning("Sem dados de vitórias/derrotas para exibir.")

# --- Dados Brutos ---
st.subheader("Histórico Detalhado")
st.dataframe(df_filtrado)
