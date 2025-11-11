from sqlalchemy import Column, Integer, String, Float, Boolean, BigInteger, ForeignKey, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import relationship, validates
from datetime import datetime
from .database import Base

class Jogador(Base):
    __tablename__ = 'jogadores'

    id = Column(Integer, primary_key=True, index=True)
    puuid = Column(String, unique=True, index=True, nullable=False)
    nome_jogador = Column(String, nullable=False)
    icone_id = Column(Integer, default=0)
    nivel = Column(Integer, default=1)

    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(datetime.timezone.utc), onupdate=datetime.now(datetime.timezone.utc), nullable=False)
    
    participacao = relationship("Participacao", back_populates="jogador", cascade="all, delete-orphan", lazy="dynamic")

    def __repr__(self):
        return f"<Jogador(id={self.id}, nome='{self.nome_jogador}', puuid='{self.puuid[:8]}...')>"
    
    @property
    def total_partidas(self):
        return self.participacoes.count()
    
    @property
    def total_vitorias(self):
        return self.participacoes.filter_by(resultado=True).count()
    
    @property
    def winrate(self):
        total = self.total_partidas
        if total == 0:
            return 0.0
        return self.total_vitorias / total
    
class Partida(Base):
    __tablename__ = 'partidas'
    
    id = Column(Integer, primary_key=True, index=True) 
    partida_id = Column(String, unique=True, index=True, nullable=False) 
    data_partida = Column(BigInteger, index = True, nullable=False) 
    duracao_partida = Column(Integer, index=True, nullable=False) 
    tipo_fila = Column(Integer, index=True, nullable=False) 
    patch = Column(String, nullable=False)

    created_at = Column(datetime, default=datetime.timezone.utc)

    participacao = relationship(
        "Participacao", 
        back_populates="partida",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    __table_args__ = (
        Index('idx_partida_tipo_data', 'tipo_fila', 'data_partida')
    )

    def __repr__(self):
        return f"<Partida(id={self.partida_id}, tipo_fila={self.tipo_fila})>"

    @validates('tipo_fila')
    def validate_duracao(self, key, value):
        if value < 0:
            raise ValueError("duração da partida deve ser positiva")
        return value
    
    @validates('tipo_fila')
    def validates_tipo_fila(self, key, value):
        filas_validas = [
            0,    # Custom
            400,  # Normal Draft
            420,  # Ranked Solo/Duo
            430,  # Normal Blind
            440,  # Ranked Flex
            450,  # ARAM
            700,  # Clash
            720,  # ARAM Clash
            830,  # Intro Bots
            840,  # Beginner Bots
            850,  # Intermediate Bots
            900,  # URF
            1020, # One for All
            1300, # Nexus Blitz
            1400, # Ultimate Spellbook
        ]
        if value in filas_validas and value != 0:
            import warnings
            warnings.warn(f"tipo de fila desconhecido: {value}")

    @property
    def duracao_formatado(self):
        minutos = self.duracao_partida // 60
        segundos = self.duracao_partida % 60
        return f"{minutos}:{segundos:02d}"
    
    @property
    def data_formatada(self):
        from datetime import datetime
        timestamp = self.data_partida / 1000
        return datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M')

class Participacao(Base):
    __tablename__ = 'participacoes'

    id = Column(Integer, primary_key=True, index=True)

    jogador_id = Column(
        Integer, 
        ForeignKey("jogadores.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )

    partida_id = Column(
        Integer, 
        ForeignKey("partidas.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )

    campeao = Column(String, nullable=False) 
    abates = Column(Integer, default=0, nullable=False) 
    mortes = Column(Integer, default=0, nullable=False) 
    assistencias = Column(Integer, default=0, nullable=False) 
    cs = Column(Integer, default=0, nullable=False)  
    resultado = Column(Boolean, nullable=False)
    posicao = Column(String, index=True)
    dano_campeoes = Column(Integer, default=0, nullable=False)
    kda = Column(Float, default=0.0, nullable=False) 
    pontuacao_visao = Column(Integer, default=0, nullable=False) 
    ouro_ganho = Column(Integer, default=0, nullable=False) 
    cs_jungle = Column(Integer, default=0, nullable=False) 
    penta_kills = Column(Integer, default=0, nullable=False) 
    quadra_kills = Column(Integer, default=0, nullable=False) 
    double_kills = Column(Integer, default=0, nullable=False) 
    fb_kill = Column(Boolean, default=False, nullable=False) 
    fb_assist = Column(Boolean, default=False, nullable=False)

    created_at = Column(datetime, default=datetime.timezone.utc)
    
    jogador = relationship("Jogador", back_populates="participacoes")
    partida = relationship("Partida", back_populates="participacoes")

    __table_args__ = (
        UniqueConstraint('jogador_id', 'partida_id', name='uix_jogador_partida'),
        
        Index('idx_jogador_resultado', 'jogador_id', 'resultado'),
        Index('idx_jogador_campeao', 'jogador_id', 'campeao'),
        Index('idx_posicao_resultado', 'posicao', 'resultado'),
    )

    def __repr__(self):
        resultado_str = "vitória" if self.resultado else "derrota"
        return (f"<Participacao(jogador_id={self.jogador_id}, campeao='{self.campeao}', {resultado_str})>")
    
@validates('abates', 'mortes', 'assistencias', 'cs', 'dano_campeoes', 'pontuacao_visao', 'ouro_gahno', 'cs_jungles')
def validate_positive(self, key, value):
    if value < 0:
        raise ValueError(f"{key} não pode ser negativo")
    return value

@validates('kda')
def validate_kda(sel, key, value):
    if value < 0:
        raise ValueError("KDA não pode ser negativo")
    if value > 100:
        import warnings
        warnings.warn(f"KDA muito alto: {value}")
    return value

@validates('posicao')
def validate_posicao(self, key, value):
    if not value:
        return None

    posicoes_validas = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY', 'MID', 'ADC', 'SUPPORT']
    value_upper = value.upper()

    normalizacao = {
        'MID': 'MIDDLE',
        'ADC': 'BOTTOM',
        'SUPPORT': 'UTILITY',
        'SUP': 'UTILITY'
    }

    value_upper = normalizacao.get(value_upper, value_upper)

    if value_upper not in posicoes_validas:
        import warnings
        warnings.warn(f"posicao desconhecida: {value}")

@property
def kda_calculado(self):
    if self.mortes == 0:
        return float(self.abates + self.assistencias)
    return (self.abates + self.assistencias) / self.mortes

@property
def kill_participation(self):
    return self.abates + self.assistencias

@property
def resultado_texto(self):
    return 'vitória' if self.resultado else 'derrota'

@property
def cs_total(self):
    return self.cs + self.cs_jungle

@property
def cs_por_minuto(self):
    if self.partida and self.partida.duracao_partida > 0:
        minutos = self.partida.duracao_partida / 60
        return self.cs_total / minutos
    return 0.0

def to_dict(self):
    return {
        'id': self.id,
        'jogador_id': self.jogador_id,
        'partida_id': self.partida_id,
        'campeao': self.campeao,
        'abates': self.abates,
        'mortes': self.mortes,
        'assistencias': self.assistencias,
        'cs': self.cs,
        'resultado': self.resultado,
        'posicao': self.posicao,
        'kda': self.kda,
        'dano_campeoes': self.dano_campeoes,
        'pontuacao_visao': self.pontuacao_visao,
        'ouro_ganho': self.ouro_ganho,
    }

