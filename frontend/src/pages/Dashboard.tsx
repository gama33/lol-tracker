import { useState } from "react"
import { apiService } from "../services/api"
import type { EstatisticasJogador, Jogador, Partida } from "../types"
import { Header } from "../components/Header"
import { PlayerInfo } from "../components/PlayerInfo"
import { PlayerStats } from "../components/PlayerStats"
import { TopChampions } from "../components/TopChampions"
import { MatchHistory } from "../components/MatchHistory"

export default function Dashboard() {
    const [searchQuery, setSearchQuery] = useState("")
    const [tagLine, setTagLine] = useState("")
    const [loading, setLoading] = useState(false)
    const [syncing, setSyncing] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [syncMessage, setSyncMessage] = useState<string | null>(null)
    const [jogador, setJogador] = useState<Jogador | null>(null)
    const [estatisticas, setEstatisticas] = useState<EstatisticasJogador | null>(null)
    const [partidas, setPartidas] = useState<Partida[]>([])

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!searchQuery.trim()) return;

        setLoading(true);
        setError(null);
        setSyncMessage(null);

        try {
            const jogadorEncontrado = await apiService.getJogadorByNome(searchQuery, tagLine);

            if (jogadorEncontrado) {
                setJogador(jogadorEncontrado);
                const stats = await apiService.obterEstatisticas(jogadorEncontrado.id);
                setEstatisticas(stats);
                const matches = await apiService.listarPartidas(jogadorEncontrado.id, undefined, 20);
                setPartidas(matches);
            }
        } catch (error: any) {
            if (error.response && error.response.status === 404) {
                setError("Jogador não encontrado. Deseja sincronizá-lo?");
            } else {
                console.error('Erro ao buscar jogador:', error);
                setError("Erro ao buscar dados do jogador. Tente novamente mais tarde.");
            }
            setJogador(null);
            setEstatisticas(null);
            setPartidas([]);
        } finally {
            setLoading(false);
        }
    };

    const handleSync = async () => {
        const nome = jogador ? jogador.nome_jogador : searchQuery;
        const tag = jogador ? jogador.tag_line : tagLine;

        if (!nome.trim() || !tag?.trim()) {
            setError("Nome de jogador e tag são obrigatórios para sincronizar.");
            return;
        }

        setSyncing(true);
        setError(null);
        setSyncMessage("Sincronizando... Isso pode levar alguns instantes.");

        try {
            const response = await apiService.sincronizarPartidas({
                nome_jogador: nome,
                tag_line: tag,
                quantidade: 20,
                apenas_ranked: false
            });
            setSyncMessage(`Sincronização concluída! ${response.partidas_sincronizadas} novas partidas adicionadas.`);
            // Automatically search for the player after syncing
            const fakeEvent = { preventDefault: () => {} } as React.FormEvent;
            await handleSearch(fakeEvent);
        } catch (error: any) {
            console.error("Erro ao sincronizar jogador:", error);
            setSyncMessage(null);
            setError(error.response?.data?.detail || "Erro ao sincronizar jogador.");
        } finally {
            setSyncing(false);
        }
    };

    return (
        <div className="min-h-screen bg-black text-[#00FF00] font-mono p-8">
            <Header
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                tagLine={tagLine}
                setTagLine={setTagLine}
                handleSearch={handleSearch}
                loading={loading || syncing}
            />

            {(loading || syncing) && (
                <div className="text-center text-[#00FF00] animate-pulse mb-8">
                    <span className="animate-pulse">█</span> {syncing ? "SINCRONIZANDO_DADOS..." : "CARREGANDO_DADOS..."}
                </div>
            )}

            {syncMessage && !error && (
                <div className="text-center text-green-400 border border-green-500 p-4 mb-8">
                    {syncMessage}
                </div>
            )}

            {error && (
                <div className="text-center text-red-500 border border-red-500 p-4 mb-8">
                    <div>[ERRO]: {error}</div>
                    {error.includes("sincronizá-lo") && (
                        <button
                            onClick={handleSync}
                            disabled={syncing}
                            className="mt-4 bg-[#00FF00] text-black font-bold py-2 px-4 hover:bg-[#00FFFF] disabled:opacity-50"
                        >
                            {syncing ? "Sincronizando..." : "Sincronizar Jogador"}
                        </button>
                    )}
                </div>
            )}

            {jogador && estatisticas && (
                <>
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                        <PlayerInfo jogador={jogador} handleSync={handleSync} syncing={syncing} />
                        <PlayerStats estatisticas={estatisticas} />
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <TopChampions estatisticas={estatisticas} />
                        <MatchHistory partidas={partidas} />
                    </div>
                </>
            )}
        </div>
    )
}