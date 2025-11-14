import { useState } from "react"
import { apiService } from "../services/api"
import type { EstatisticasJogador, Jogador, Partida } from "../types"
import { Header } from "../components/Header"
import { SearchBar } from "../components/SearchBar"
import { PlayerInfo } from "../components/PlayerInfo"
import { PlayerStats } from "../components/PlayerStats"
import { TopChampions } from "../components/TopChampions"
import { MatchHistory } from "../components/MatchHistory"

export default function Dashboard() {
    const [searchQuery, setSearchQuery] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [jogador, setJogador] = useState<Jogador | null>(null)
    const [estatisticas, setEstatisticas] = useState<EstatisticasJogador | null>(null)
    const [partidas, setPartidas] = useState<Partida[]>([])

    const handleSearch = async () => {
        if (!searchQuery.trim()) return

        setLoading(true)
        setError(null)
        try {
            const jogadores = await apiService.buscarJogadores(100); // Fetch up to 100 players
            if (jogadores.length > 0) {
                const jogadorEncontrado = jogadores.find(j => j.nome_jogador.toLowerCase() === searchQuery.toLowerCase())
                if (jogadorEncontrado) {
                    setJogador(jogadorEncontrado)
                    const stats = await apiService.obterEstatisticas(jogadorEncontrado.id)
                    setEstatisticas(stats)
                    const matches = await apiService.listarPartidas(jogadorEncontrado.id, undefined, 5)
                    setPartidas(matches)
                } else {
                    setError("Jogador não encontrado.")
                    setJogador(null)
                    setEstatisticas(null)
                    setPartidas([])
                }
            } else {
                setError("Nenhum jogador encontrado.")
                setJogador(null)
                setEstatisticas(null)
                setPartidas([])
            }
        } catch (error) {
            console.error('Erro ao buscar jogador:', error)
            setError("Erro ao buscar dados do jogador. Tente novamente mais tarde.")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-black text-[#00FF00] font-mono p-8">
            <Header />
            <SearchBar
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                handleSearch={handleSearch}
                loading={loading}
            />

            {loading && (
                <div className="text-center text-[#00FF00] animate-pulse mb-8">
                    <span className="animate-pulse">█</span> CARREGANDO_DADOS...
                </div>
            )}

            {error && (
                <div className="text-center text-red-500 border border-red-500 p-4 mb-8">
                    [ERRO]: {error}
                </div>
            )}

            {jogador && estatisticas && (
                <>
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                        <PlayerInfo jogador={jogador} />
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
