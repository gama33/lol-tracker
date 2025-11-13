import { Search, Terminal, ChevronRight } from "lucide-react"
import { useEffect, useState } from "react"
import { apiService } from "../services/api"
import type { EstatisticasJogador, Jogador, Partida } from "../types"

export default function Dashboard() {
    const [time, setTime] = useState(new Date())
    const [searchQuery, setSearchQuery] = useState("")
    const [loading, setLoading] = useState(false)
    const [jogador, setJogador] = useState<Jogador | null>(null)
    const [estatisticas, setEstatisticas] = useState<EstatisticasJogador | null>(null)
    const [partidas, setPartidas] = useState<Partida[]>([])

    useEffect(() => {
        const timer = setInterval(() => setTime(new Date()), 1000)
        return () => clearInterval(timer)
    }, [])

    const handleSearch = async () => {
        if (!searchQuery.trim()) return

        setLoading(true)
        try {
            const jogadores = await apiService.buscarJogadores(1)
            if (jogadores.length > 0){
                setJogador(jogadores[0])
                const stats = await apiService.obterEstatisticas(jogadores[0].id)
                setEstatisticas(stats)
                const matches = await apiService.listarPartidas(jogadores[0].id, undefined, 5)
                setPartidas(matches)
            }
        } catch (error) {
            console.error('Erro ao buscar jogador:', error)
        } finally {
            setLoading(false)
        }
    }
    const formatKDA = (abates: number, mortes: number, assistencias: number) => {
        return `${abates}/${mortes}/${assistencias}`
    }

    const formatTimeAgo = (timestamp: number) => {
        const diff = Date.now() - timestamp
        const hours = Math.floor(diff / (1000 * 60 * 60))
        const days = Math.floor(hours / 24)

        if (days > 0) return `${days}d ago`
        if (hours > 0) return `${hours}h ago`
        return 'now'
    }

    return(
        <div className="min-h-screen bg-black text-[#00FF00] font-mono p-8">
      <div className="border border-[#00FF00] mb-8">
        <div className="bg-[#00FF00] text-black px-4 py-2 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Terminal className="w-4 h-4" />
            <span className="font-bold">MATCH_TRACKER.EXE</span>
          </div>
          <div className="text-xs">{time.toLocaleTimeString()}</div>
        </div>
        <div className="p-6">
          <div className="mb-4">
            <span className="text-[#00FF00]">root@tracker:~$</span>{" "}
            <span className="text-white">query --player</span>
          </div>
          <div className="relative">
            <input
              type="text"
              placeholder="Enter summoner name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              disabled={loading}
              className="w-full bg-black border border-[#00FF00] p-4 text-[#00FF00] font-mono placeholder:text-[#00FF00]/40 focus:outline-none focus:border-[#00FFFF] focus:shadow-[0_0_10px_rgba(0,255,0,0.5)] disabled:opacity-50"
            />
            <button
              onClick={handleSearch}
              disabled={loading}
              className="absolute right-4 top-1/2 -translate-y-1/2"
            >
              <Search className="w-5 h-5 text-[#00FF00] hover:text-[#00FFFF] cursor-pointer" />
            </button>
          </div>
        </div>
      </div>

      {loading && (
        <div className="text-center text-[#00FF00] animate-pulse mb-8">
          <span className="animate-pulse">█</span> LOADING_DATA...
        </div>
      )}

      {jogador && estatisticas && (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            {/* Player Info */}
            <div className="border border-[#00FF00] p-6">
              <div className="text-[#00FFFF] mb-4">[PLAYER_DATA]</div>
              <div className="space-y-2 text-sm">
                <div>
                  <span className="text-[#00FF00]">{">"}</span> NAME:{" "}
                  <span className="text-white">{jogador.nome_jogador.toUpperCase()}</span>
                </div>
                <div>
                  <span className="text-[#00FF00]">{">"}</span> LEVEL:{" "}
                  <span className="text-white">{jogador.nivel}</span>
                </div>
                <div>
                  <span className="text-[#00FF00]">{">"}</span> ICON_ID:{" "}
                  <span className="text-white">{jogador.icone_id}</span>
                </div>
                <div>
                  <span className="text-[#00FF00]">{">"}</span> STATUS:{" "}
                  <span className="text-[#00FF00] animate-pulse">TRACKED</span>
                </div>
              </div>
            </div>

            {/* Stats */}
            <div className="lg:col-span-2 border border-[#00FF00]">
              <div className="bg-[#00FF00] text-black px-4 py-2 font-bold">
                [PERFORMANCE_METRICS]
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 divide-x divide-[#00FF00]">
                <div className="p-6 text-center">
                  <div className="text-xs mb-2 text-[#00FFFF]">WIN_RATE</div>
                  <div className="text-4xl font-bold text-[#00FF00]">
                    {Math.round(estatisticas.winrate * 100)}%
                  </div>
                </div>
                <div className="p-6 text-center">
                  <div className="text-xs mb-2 text-[#00FFFF]">KDA_RATIO</div>
                  <div className="text-4xl font-bold text-[#00FF00]">
                    {estatisticas.kda_medio.toFixed(1)}
                  </div>
                </div>
                <div className="p-6 text-center">
                  <div className="text-xs mb-2 text-[#00FFFF]">TOTAL_GAMES</div>
                  <div className="text-4xl font-bold text-white">
                    {estatisticas.total_partidas}
                  </div>
                </div>
                <div className="p-6 text-center">
                  <div className="text-xs mb-2 text-[#00FFFF]">AVG_CS</div>
                  <div className="text-4xl font-bold text-white">
                    {Math.round(estatisticas.cs_medio)}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Top Champions */}
            <div className="border border-[#00FF00]">
              <div className="bg-[#00FF00] text-black px-4 py-2 font-bold">
                [TOP_CHAMPIONS]
              </div>
              <div className="p-6 space-y-3">
                {estatisticas.top_campeoes?.slice(0, 5).map((champ, i) => (
                  <div
                    key={i}
                    className="flex items-center justify-between text-sm border-l-2 border-[#00FF00] pl-3"
                  >
                    <div className="flex items-center gap-2">
                      <ChevronRight className="w-4 h-4 text-[#00FF00]" />
                      <div>
                        <div className="text-white font-bold">{champ.campeao}</div>
                        <div className="text-[#00FF00]/60">{champ.partidas} matches</div>
                      </div>
                    </div>
                    <div className="text-[#00FFFF] font-bold">
                      {Math.round(champ.winrate * 100)}%
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Match History */}
            <div className="lg:col-span-2 border border-[#00FF00]">
              <div className="bg-[#00FF00] text-black px-4 py-2 font-bold">
                [MATCH_HISTORY]
              </div>
              <div className="p-6 space-y-3">
                {partidas.length === 0 ? (
                  <div className="text-[#00FF00]/60 text-center p-8">
                    NO_MATCHES_FOUND
                  </div>
                ) : (
                  partidas.map((partida, i) => (
                    <div
                      key={i}
                      className="flex items-center justify-between p-4 border border-[#00FF00] bg-[#00FF00]/5"
                    >
                      <div className="flex items-center gap-6">
                        <div className="text-2xl font-bold text-[#00FF00]">
                          [MATCH]
                        </div>
                        <div>
                          <div className="text-white font-bold">
                            {partida.partida_id}
                          </div>
                          <div className="text-[#00FF00]/60 text-xs">
                            {formatTimeAgo(partida.data_partida)}
                          </div>
                        </div>
                      </div>
                      <div className="flex gap-6 text-sm">
                        <div>
                          <div className="text-[#00FFFF]">DURATION:</div>
                          <div className="text-white">
                            {Math.floor(partida.duracao_partida / 60)}m
                          </div>
                        </div>
                        <div>
                          <div className="text-[#00FFFF]">QUEUE:</div>
                          <div className="text-white">{partida.tipo_fila}</div>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
              <div className="border-t border-[#00FF00] p-4 text-xs text-[#00FF00]/60">
                <span className="animate-pulse">█</span> STREAMING_DATA...
              </div>
            </div>
          </div>
        </>
      )}
    </div>
    )
}