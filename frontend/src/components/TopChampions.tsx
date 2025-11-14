import { ChevronRight } from "lucide-react"
import type { EstatisticasJogador } from "../types"

interface TopChampionsProps {
    estatisticas: EstatisticasJogador
}

export const TopChampions = ({ estatisticas }: TopChampionsProps) => {
    return (
        <div className="border border-[#00FF00]">
            <div className="bg-[#00FF00] text-black px-4 py-2 font-bold">
                [TOP_CAMPEÕES]
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
                                <div className="text-[#00FF00]/60">{champ.partidas} partidas</div>
                            </div>
                        </div>
                        <div className="text-[#00FFFF] font-bold">
                            {Math.round(champ.winrate * 100)}%
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}