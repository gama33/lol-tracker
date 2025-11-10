from sqlalchemy import Column, Integer, String, Float, Boolean, BigInteger, ForeignKey 
from .database import Base
from sqlalchemy.orm import declarative_base, relationship

class Jogador(Base):
    __tablename__ = 'jogadores'

    id = Column(Integer, primary_key=True, index=True)
    puuid = Column(String, unique=True, index=True)
    nome_jogador = Column(String)
    icone_id = Column(Integer)
    nivel = Column(Integer)
    
    participacao = relationship("Participacao", back_populates="jogador")

class Partida(Base):
    __tablename__ = 'partidas'
    
    id = Column(Integer, primary_key=True, index=True) 
    partida_id = Column(String, unique=True, index=True) 
    data_partida = Column(BigInteger, index = True) 
    duracao_partida = Column(Integer) 
    tipo_fila = Column(Integer, index=True) 
    patch = Column(String) 

    participacao = relationship("Participacao", back_populates="partida")

class Participacao(Base):
    __tablename__ = 'participacoes'

    id = Column(Integer, primary_key=True, index=True)

    jogador_id = Column(Integer, ForeignKey("jogadores.id"), index=True)
    partida_id = Column(Integer, ForeignKey("partidas.id"), index=True)

    campeao = Column(String) 
    abates = Column(Integer) 
    mortes = Column(Integer) 
    assistencias = Column(Integer) 
    cs = Column(Integer)  
    resultado = Column(Boolean) 
    posicao = Column(String, index=True) 
    dano_campeoes = Column(Integer) 
    kda = Column(Float) 
    pontuacao_visao = Column(Integer) 
    ouro_ganho = Column(Integer) 
    cs_jungle = Column(Integer) 
    penta_kills = Column(Integer) 
    quadra_kills = Column(Integer) 
    double_kills = Column(Integer) 
    fb_kill = Column(Boolean) 
    fb_assist = Column(Boolean) 
    
    jogador = relationship("Jogador", back_populates="participacao")
    partida = relationship("Partida", back_populates="participacao")