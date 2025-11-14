import type { Jogador } from "../types"

interface PlayerInfoProps {
    jogador: Jogador;
    handleSync: () => void;
    syncing: boolean;
}

export const PlayerInfo = ({ jogador, handleSync, syncing }: PlayerInfoProps) => {
    return (
        <div className="border border-[#00FF00] p-6 flex flex-col justify-between">
            <div className="flex-grow">
                <div className="text-[#00FFFF] mb-4">[DADOS_JOGADOR]</div>
                <div className="space-y-2 text-sm">
                    <div>
                        <span className="text-[#00FF00]">{">"}</span> NOME:{" "}
                        <span className="text-white">{jogador.nome_jogador.toUpperCase()}#{jogador.tag_line}</span>
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
            <div className="mt-4">
                <button
                    onClick={handleSync}
                    disabled={syncing}
                    className="w-full bg-[#00FF00] text-black font-bold py-2 px-4 hover:bg-[#00FFFF] disabled:opacity-50"
                >
                    {syncing ? "Sincronizando..." : "Sincronizar Perfil"}
                </button>
            </div>
        </div>
    )
}