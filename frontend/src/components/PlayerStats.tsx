import type { EstatisticasJogador } from "../types"

interface PlayerStatsProps {
    estatisticas: EstatisticasJogador
}

export const PlayerStats = ({ estatisticas }: PlayerStatsProps) => {
    return (
        <div className="lg:col-span-2 border border-[#00FF00]">
            <div className="bg-[#00FF00] text-black px-4 py-2 font-bold">
                [MÉTRICAS_DESEMPENHO]
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 divide-x divide-[#00FF00]">
                <div className="p-6 text-center">
                    <div className="text-xs mb-2 text-[#00FFFF]">TAXA_VITÓRIA</div>
                    <div className="text-4xl font-bold text-[#00FF00]">
                        {Math.round(estatisticas.winrate * 100)}%
                    </div>
                </div>
                <div className="p-6 text-center">
                    <div className="text-xs mb-2 text-[#00FFFF]">KDA_MÉDIO</div>
                    <div className="text-4xl font-bold text-[#00FF00]">
                        {estatisticas.kda_medio.toFixed(1)}
                    </div>
                </div>
                <div className="p-6 text-center">
                    <div className="text-xs mb-2 text-[#00FFFF]">TOTAL_PARTIDAS</div>
                    <div className="text-4xl font-bold text-white">
                        {estatisticas.total_partidas}
                    </div>
                </div>
                <div className="p-6 text-center">
                    <div className="text-xs mb-2 text-[#00FFFF]">CS_MÉDIO</div>
                    <div className="text-4xl font-bold text-white">
                        {Math.round(estatisticas.cs_medio)}
                    </div>
                </div>
            </div>
        </div>
    )
}
