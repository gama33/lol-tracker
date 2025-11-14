export interface Jogador {
  id: number;
  puuid: string;
  nome_jogador: string;
  tag_line?: string;
  icone_id: number;
  nivel: number;
  criado_em: string;
  total_partidas?: number;
  total_vitorias?: number;
  winrate?: number;
}

export interface Partida {
  id: number;
  partida_id: string;
  data_partida: number;
  duracao_partida: number;
  tipo_fila: number;
  patch: string;
  criado_em: string;
  participacao?: Participacao;
}

export interface Participacao {
  id: number;
  jogador_id: number;
  partida_id: number;
  campeao: string;
  campeao_icone_url?: string;
  abates: number;
  mortes: number;
  assistencias: number;
  cs: number;
  resultado: boolean;
  posicao: string;
  dano_campeoes: number;
  kda: number;
  pontuacao_visao: number;
  ouro_ganho: number;
  cs_jungle: number;
  penta_kills: number;
  quadra_kills: number;
  double_kills: number;
  fb_kill: boolean;
  fb_assist: boolean;
}

export interface PartidaDetalhada extends Partida {
  participacoes: Participacao[];
}

export interface TopCampeao {
  campeao: string;
  partidas: number;
  vitorias: number;
  derrotas: number;
  winrate: number;
  kda_medio: number;
}

export interface DistribuicaoPosicao {
  partidas: number;
  percentual: number;
}

export interface EstatisticasJogador {
  jogador_id: number;
  nome_jogador: string;
  total_partidas: number;
  total_vitorias: number;
  total_derrotas: number;
  winrate: number;
  kda_medio: number;
  abates_medio: number;
  mortes_medio: number;
  assistencias_medio: number;
  cs_medio: number;
  dano_medio: number;
  ouro_medio: number;
  top_campeoes?: TopCampeao[];
  posicoes?: Record<string, DistribuicaoPosicao>;
}

export interface SincronizarRequest {
  nome_jogador?: string;
  tag_line?: string;
  quantidade: number;
  apenas_ranked: boolean;
}

export interface SincronizarResponse {
  status: string;
  partidas_sincronizadas: number;
  partidas_duplicadas: number;
  erros: string[];
  tempo_execucao: number;
}