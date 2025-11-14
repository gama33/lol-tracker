import type { Partida } from "../types"
import { MatchCard } from "./MatchCard"

interface MatchHistoryProps {
    partidas: Partida[]
}

export const MatchHistory = ({ partidas }: MatchHistoryProps) => {
    return (
        <div className="lg:col-span-2 border border-[#00FF00]">
            <div className="bg-[#00FF00] text-black px-4 py-2 font-bold">
                [HISTÓRICO_PARTIDAS]
            </div>
            <div className="p-6 space-y-3">
                {partidas.length === 0 ? (
                    <div className="text-[#00FF00]/60 text-center p-8">
                        NENHUMA_PARTIDA_ENCONTRADA
                    </div>
                ) : (
                    partidas.map((partida, i) => (
                        <MatchCard key={i} partida={partida} />
                    ))
                )}
            </div>
            <div className="border-t border-[#00FF00] p-4 text-xs text-[#00FF00]/60">
                <span className="animate-pulse">█</span> TRANSMITINDO_DADOS...
            </div>
        </div>
    )
}

