import type { Partida } from "../types"
import { formatKDA, formatTimeAgo } from "../utils/formatters"

interface MatchCardProps {
    partida: Partida
}

export const MatchCard = ({ partida }: MatchCardProps) => {
    const { participacao } = partida

    if (!participacao) {
        return null // Should not happen with the backend changes, but good for safety
    }

    const isVictory = participacao.resultado
    const cardColorClass = isVictory ? "border-green-500 bg-green-900/20" : "border-red-500 bg-red-900/20"
    const textColorClass = isVictory ? "text-green-400" : "text-red-400"

    return (
        <div className={`flex flex-col md:flex-row items-center justify-between p-4 border ${cardColorClass} transition-all duration-300 hover:shadow-[0_0_15px_rgba(0,255,0,0.7)] hover:scale-[1.01]`}>
            <div className="flex items-center gap-4 mb-4 md:mb-0">
                {/* Champion Icon (Placeholder) */}
                <div className="w-12 h-12 bg-gray-700 rounded-full flex items-center justify-center text-xs font-bold">
                    {participacao.campeao.slice(0, 2).toUpperCase()}
                </div>
                <div>
                    <div className="text-white font-bold text-lg">{participacao.campeao}</div>
                    <div className={`text-sm ${textColorClass}`}>
                        {isVictory ? "VITÓRIA" : "DERROTA"} - {formatTimeAgo(partida.data_partida)}
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm text-center md:grid-cols-4 lg:grid-cols-5">
                <div>
                    <div className="text-[#00FFFF]">KDA:</div>
                    <div className="text-white">{formatKDA(participacao.abates, participacao.mortes, participacao.assistencias)}</div>
                </div>
                <div>
                    <div className="text-[#00FFFF]">DANO:</div>
                    <div className="text-white">{participacao.dano_campeoes.toLocaleString()}</div>
                </div>
                <div>
                    <div className="text-[#00FFFF]">CS:</div>
                    <div className="text-white">{participacao.cs}</div>
                </div>
                <div>
                    <div className="text-[#00FFFF]">OURO:</div>
                    <div className="text-white">{participacao.ouro_ganho.toLocaleString()}</div>
                </div>
                <div className="hidden lg:block">
                    <div className="text-[#00FFFF]">POSIÇÃO:</div>
                    <div className="text-white">{participacao.posicao || "N/A"}</div>
                </div>
            </div>
        </div>
    )
}
