# esse arquivo terá a "preocupação" de descrever a "forma" da nossa tabela.
# importação dos modulos
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# cria uma classe Base para os modelos usarem
Base = declarative_base()

# modelo para a tabela de partidas
class Partida(Base): # define o modelo - cada instancia dessa classe representa uma linha na tabela de partidas
    __tablename__ = 'partidas' # define o nome da tabela no banco de dados
    
    id = Column(Integer, primary_key=True, index=True) # id unico para cada linha
    partida_id = Column(String, unique=True, index=True) # id da partida
    campeao = Column(String) # campeão
    abates = Column(Integer) # abates
    mortes = Column(Integer) # mortes
    assistencias = Column(Integer) # assistencias
    cs = Column(Integer)  # minions + monstros
    resultado = Column(String)  # 'Vitoria' ou 'Derrota'    
