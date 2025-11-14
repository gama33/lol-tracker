import axios from 'axios';
import type {
    Jogador,
    EstatisticasJogador,
    Partida,
    PartidaDetalhada,
    SincronizarRequest,
    SincronizarResponse
} from '../types';

const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const apiService = {
    async buscarJogadores(limit: number = 50): Promise<Jogador[]> {
        const { data } = await api.get(`/jogadores?limit=${limit}`);
        return data;
    },

    async obterJogador(id: number): Promise<Jogador> {
        const { data } = await api.get(`/jogadores/${id}`);
        return data;
    },

    async obterEstatisticas(id: number, tipoFila?: number): Promise<EstatisticasJogador> {
        const params = tipoFila ? `?tipo_fila=${tipoFila}` : '';
        const { data } = await api.get(`/jogadores/${id}/estatisticas${params}`);
        return data;
    },

    async listarPartidas(jogadorId?: number, tipoFila?: number, limit: number= 20): Promise<Partida[]> {
        const params = new URLSearchParams();
        if (jogadorId) params.append('jogador_id', jogadorId.toString());
        if (tipoFila) params.append('tipo_fila', tipoFila.toString());
        params.append('limit', limit.toString());

        const { data } = await api.get(`/partidas?${params}`);
        return data;
    },

    async obterPartida(id: number): Promise<PartidaDetalhada> {
        const { data } = await api.get(`/partidas/${id}`);
        return data;
    },

    async sincronizarPartidas(request: SincronizarRequest): Promise<SincronizarResponse> {
        const { data } = await api.post('/sincronizar-partidas', request);
        return data;
    },

    async healthCheck(): Promise<{ status: string; api: string; database: string}> {
        const { data } = await api.get('/health');
        return data;
    }
};