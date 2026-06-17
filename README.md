# league-tracker

Um projeto pessoal de Engenharia e Análise de Dados focado em extrair, estruturar e visualizar históricos de partidas de League of Legends utilizando a **API oficial da Riot Games**.

## Visão Geral do Projeto

O objetivo deste projeto é criar um pipeline de dados completo (ETL) que transforma dados brutos de partidas individuais (JSON) em insights visuais acionáveis através de um painel interativo no Power BI.


### 🛠️ Tecnologias Utilizadas

* **Python 3** (Linguagem principal, desenvolvido e testado na versão 3.13.9)
* **Requests & Dotenv** (Consumo da API da Riot Games e segurança de chaves)
* **Pandas** (Tratamento, limpeza e manipulação de dados brutos)
* **SQLAlchemy** (Abstração e carga dos dados no banco relacionais)
* **SQLite** (Armazenamento local unificado dos dados das partidas)
* **Matplotlib & Seaborn** (Visualização de Dados para gerar gráficos estatísticos rápidos e análises exploratórias)
* **Jupyter Notebook** (Ambiente iterativo utilizado para prototipagem de código)
* **Power BI** (Criação de dashboards e análise visual de métricas)

## 📁 Estrutura do Repositório

* `puuid.py`: Script responsável por buscar o PUUID do jogador.
* `extract.py`: Script que vai consumir os IDs das partidas recentes e baixar os arquivos JSON detalhados (com controle de *Rate Limit* e cache local).
* `analysis.py`: Esse módulo varre os JSONs locais, filtra os dados específicos do jogador alvo e calcula métricas derivadas (como KDA exato e Gold por Minuto).

O `analysis.py` ainda faz a conexão com um banco de dados SQLite, além de permitir análises mais rápidas com Pandas e Jupyter

## ⚙️ Como Executar

### Pré-requisitos
* Python 3.10 (ou superior) instalado
* Uma chave de API da Riot Games ativa (Riot Developer Portal)

### Configuração
1. Clone o repositório:
   ```bash
   git clone [https://github.com/joaoksaas/lol-tracker.git](https://github.com/joaoksaas/lol-tracker.git)

2. Instale as dependências necessárias:
   ```bash
   pip install requests python-dotenv pandas sqlalchemy matplotlib seaborn notebook

3. Crie um arquivo ```.env``` na raiz do projeto, semelhante ao ```.env.example```:
  ```bash
  RIOT_API_KEY = "sua_api_key"
  NICK = "nick_da_conta"
  RIOT_ID = "riot_id_da_conta"

   
