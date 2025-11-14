# LolTracker
Este é um projeto de estudo focado na criação de uma aplicação web para análise de desempenho em League of Legends, baseada em dados analisados do histórico de partidas. O objetivo é automatizar e modernizar a funcionalidade de uma planilha de registo manual, utilizando a API oficial da Riot Games.
## Práticas e Tecnologias

Uma das intenções neste projeto é adquirir boas práticas de desenvolvimento, como a "Separação de Preocupações" (Separation of Concerns), que consiste em definir um arquivo para cada "preocupação" do projeto.

**Back-end:** 
- **Framework:** **FastAPI** para construir as APIs com Python, juntamente com Uvicorn para implementação do servidor web.
- **Banco de Dados:** **SQLite** com a biblioteca **SQLAlchemy** para fazer a interação entre o código Python e o banco de dados.
- **Segurança:** As chaves de API são geridas de forma segura através de variáveis de ambiente, carregadas a partir de um ficheiro .env (que é ignorado pelo Git através do .gitignore).

**Estrutura do Backend:** 
- `main.py`: Ponto de entrada da aplicação. Carrega as variáveis de ambiente e define as rotas da API.
- `riot_api.py`: Módulo responsável por toda a comunicação com as APIs externas da Riot Games.
- `models.py`: Responsável por descrever a "forma" dos nossos dados (o schema das tabelas do banco de dados).
- `database.py`: Responsável por gerenciar a conexão com o banco de dados (a engine e a sessão).

## Rodando localmente


1.  Clone o repositório e entre na pasta principal:
```
git clone https://github.com/gama33/lol-tracker
cd lol-tracker
```

2.  Navegue para a pasta do backend para configurar o ambiente:
```
cd backend
```

3. Crie e ative um ambiente virtual:
```
# Crie o venv
python -m venv venv

# Ative o venv (Windows)
.\venv\Scripts\activate

# Ative o venv (Mac/Linux)
source venv/bin/activate
```

4. Instale todas as dependências:
```
pip install -r requirements.txt
```

5. Crie um documento chamado .env na pasta backend.
```
touch .env
```

6. Adicione a sua chave da API ao ficheiro .env:
```
RIOT_API_KEY="SUA_CHAVE_API_VEM_AQUI"
```

7. Volte para a pasta principal e inicie o servidor:
```
# Volte para a pasta lol-tracker
cd ..

# Inicie o servidor
uvicorn backend.main:app --reload
```
