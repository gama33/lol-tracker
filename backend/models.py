# esse arquivo terá a "preocupação" de descrever o modelo da nossa tabela.
# importação dos modulos
from sqlalchemy import Column, Integer, String, Float, Boolean, BigInteger, ForeignKey 
from .database import Base
from sqlalchemy.orm import declarative_base, relationship

# cria uma classe Base para os modelos usarem
Base = declarative_base()

class Jogador(Base):
    __tablename__ = 'jogadores'

    id = Column(Integer, primary_key=True, index=True) #id do jogaor no banco de dados
    puuid = Column(String, unique=True, index=True) #puuid do jogador
    nome_jogador = Column(String) # nome do jogador
    icone_id = Column(Integer) #id do icone do jogador

    # Esta é a ligação "virtual" para as partidas.
    # Diz: "Eu tenho muitas 'Partidas', e a forma de as encontrar
    # é através do campo 'jogador' na outra classe."
    partidas = relationship("Partida", back_populates="jogador")

# modelo para a tabela de partidas
class Partida(Base): # define o modelo - cada instancia dessa classe representa uma linha na tabela de partidas
    __tablename__ = 'partidas' # define o nome da tabela no banco de dados
    
    id = Column(Integer, primary_key=True, index=True) # id unico para cada linha
    partida_id = Column(String, unique=True, index=True) # id da partida, unique=True para evitar duplicatas
    campeao = Column(String) # campeão
    abates = Column(Integer) # abates
    mortes = Column(Integer) # mortes
    assistencias = Column(Integer) # assistencias
    cs = Column(Integer)  # minions
    resultado = Column(String)  # 'Vitoria' ou 'Derrota'
    data_partida = Column(BigInteger, index = True) # timestamp (numero grande)
    duracao_partida = Column(Integer) # em segundos
    tipo_fila = Column(Integer, index=True) # id da fila (ranked, normla, aram, etc)
    patch = Column(String) # versao do jogo
    posicao = Column(String, index=True) # rota (mid, top, etc)
    dano_campeoes = Column(Integer) # dano dado na partida
    kda = Column(Float) # KDA calculado
    pontuacao_visao = Column(Integer) # pontuação de visao
    ouro_ganho = Column(Integer) # ouro total arrecadado ao longo da partida
    cs_jungle = Column(Integer) # minions neutros da selva
    penta_kills = Column(Integer) # quantidade de penta kills
    quadra_kills = Column(Integer) # quantidade de quadra kills
    double_kills = Column(Integer) # quantidade de double kills
    fb_kill = Column(Boolean) # se participou do first blood
    fb_assist = Column(Boolean) # se pegou o first blood 
    
    # Relação inversa: cada partida está associada a um jogador, 
    jogador_id = Column(Integer, ForeignKey("jogadores.id"))

    # correspondente ao campo 'partidas' na classe Jogador.
    jogador = relationship("Jogador", back_populates="partidas")
