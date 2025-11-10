from wsgiref import validate
from sqlalchemy import Column, Integer, String, Float, Boolean, BigInteger, ForeignKey, UniqueConstraint, Index 
from datetime import datetime
from .database import Base
from sqlalchemy.orm import relationship

class Jogador(Base):
    __tablename__ = 'jogadores'

    id = Column(Integer, primary_key=True, index=True)
    puuid = Column(String, unique=True, index=True)
    nome_jogador = Column(String, nullable=False)
    icone_id = Column(Integer, default=0)
    nivel = Column(Integer, default=1)
    created_at = Column(datetime, default=datetime.timezone.utc)
    updated_at = Column(datetime, default=datetime.timezone.utc, onupdate=datetime.timezone.utc)
    
    participacao = relationship("Participacao", back_populates="jogador")

    def __repr__(self):
        return f"<Jogador(nome={self.nome_jogador}, puuid={self.puuid})>"
    
class Partida(Base):
    __tablename__ = 'partidas'
    
    id = Column(Integer, primary_key=True, index=True) 
    partida_id = Column(String, unique=True, index=True, nullable=False) 
    data_partida = Column(BigInteger, index = True, nullable=False) 
    duracao_partida = Column(Integer, index=True, nullable=False) 
    tipo_fila = Column(Integer, index=True, nullable=False) 
    patch = Column(String, nullable=False)
    created_at = Column(datetime, default=datetime.timezone.utc)

    participacao = relationship("Participacao", back_populates="partida")

    def __repr__(self):
        return f"<Partida(id={self.partida_id}, data_partida={self.data_partida})>"

class Participacao(Base):
    __tablename__ = 'participacoes'

    id = Column(Integer, primary_key=True, index=True)

    jogador_id = Column(Integer, ForeignKey("jogadores.id", ondelete="CASCADE"), nullable=False, index=True)
    partida_id = Column(Integer, ForeignKey("partidas.id", ondelete="CASCADE"), nullable=False, index=True)

    campeao = Column(String, nullable=False) 
    abates = Column(Integer, default=0) 
    mortes = Column(Integer, default=0) 
    assistencias = Column(Integer, default=0) 
    cs = Column(Integer, default=0)  
    resultado = Column(Boolean, nullable=False) 
    posicao = Column(String, index=True) 
    dano_campeoes = Column(Integer, default=0) 
    kda = Column(Float, default=0.0) 
    pontuacao_visao = Column(Integer, default=0) 
    ouro_ganho = Column(Integer, default=0) 
    cs_jungle = Column(Integer, default=0) 
    penta_kills = Column(Integer, default=0) 
    quadra_kills = Column(Integer, default=0) 
    double_kills = Column(Integer, default=0) 
    fb_kill = Column(Boolean, default=False) 
    fb_assist = Column(Boolean, default=False) 
    created_at = Column(datetime, default=datetime.timezone.utc)
    
    jogador = relationship("Jogador", back_populates="participacoes")
    partida = relationship("Partida", back_populates="participacoes")

    __table_args__ = (
        UniqueConstraint('jogador_id', 'partida_id', name='uix_jogador_partida'),
        Index('ix_jogador_resultado', 'jogador_id', 'resultado'),
        Index('ix_jogador_partida', 'partida_id', 'posicao'),
    )

    def __repr__(self):
        return f"<Participacao(jogador_id={self.jogador_id}, partida_id={self.partida_id}, campeao={self.campeao})>"