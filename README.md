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

* `puuid.py`: Script responsável por buscar o PUUID do jogador através da API da Riot utilizando o Riot ID e Tag.
* `extract.py`: Script que consome os IDs das partidas recentes e baixa os arquivos JSON detalhados (com controle de *Rate Limit* e cache local).
* `load.py`: Script de ETL que varre os JSONs locais, filtra os dados específicos do jogador alvo, calcula métricas derivadas (como KDA exato e Gold por Minuto) e centraliza tudo em tabelas relacionais no banco de dados SQLite de forma incremental e sem duplicatas.
* `analysis.py`: Módulo focado em análises exploratórias e estatísticas rápidas utilizando Pandas, Jupyter Notebook, Matplotlib e Seaborn diretamente sobre o banco de dados.

## ⚙️ Como Executar

### Pré-requisitos
* Python 3.10 (ou superior) instalado
* Uma chave de API da Riot Games ativa (Riot Developer Portal)

### Configuração
1. Clone o repositório:
   ```bash
   git clone https://github.com/joaoksaas/league-tracker.git

2. Instale as dependências necessárias:
   ```bash
   pip install requests python-dotenv pandas sqlalchemy matplotlib seaborn notebook

3. Crie um arquivo ```.env``` na raiz do projeto, semelhante ao ```.env.example```:
   ```bash
   RIOT_API_KEY="sua_api_key"
   NOME="nome_da_sua_conta"
   TAG="sua_tag_sem_o_hashtag"

   
