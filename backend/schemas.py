from pydantic import BaseModel

# dados que vamos receber do nosso frontend
class JogadorCreate(BaseModel):
    nome_jogador: str
    tag_line: str