# esse arquivo terá a "preocupação" de gerenciar a conexão com o banco de dados.
# importação dos modulos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexão com o banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./lol-tracker.db"

# cria a 'engine' do SQLAlchemy
# 'engine' é o "motor" que o SQLAlchemy usa para se comunicar com o banco de dados.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
) 

# cria uma classe para a sessão do banco de dados
# 'SessionLocal' é a configuração para criar sessões de comunicação com o banco. Pense em cada sessão como uma conversa temporária
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# cria uma classe Base para usar nos modelos (como em models.py)
Base = declarative_base()