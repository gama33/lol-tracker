import type { Jogador } from "../types"

interface PlayerInfoProps {
    jogador: Jogador
}

export const PlayerInfo = ({ jogador }: PlayerInfoProps) => {
    return (
        <div className="border border-[#00FF00] p-6">
            <div className="text-[#00FFFF] mb-4">[DADOS_JOGADOR]</div>
            <div className="space-y-2 text-sm">
                <div>
                    <span className="text-[#00FF00]">{">"}</span> NOME:{" "}
                    <span className="text-white">{jogador.nome_jogador.toUpperCase()}</span>
                </div>
                <div>
                    <span className="text-[#00FF00]">{">"}</span> NÍVEL:{" "}
                    <span className="text-white">{jogador.nivel}</span>
                </div>
                <div>
                    <span className="text-[#00FF00]">{">"}</span> ID_ICONE:{" "}
                    <span className="text-white">{jogador.icone_id}</span>
                </div>
                <div>
                    <span className="text-[#00FF00]">{">"}</span> STATUS:{" "}
                    <span className="text-[#00FF00] animate-pulse">RASTREADO</span>
                </div>
            </div>
        </div>
    )
}