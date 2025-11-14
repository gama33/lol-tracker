import { Search, Terminal } from "lucide-react"
import { useEffect, useState } from "react"

interface HeaderProps {
    searchQuery: string;
    setSearchQuery: (query: string) => void;
    tagLine: string;
    setTagLine: (tag: string) => void;
    handleSearch: (e: React.FormEvent) => void;
    loading: boolean;
}

export const Header = ({
    searchQuery,
    setSearchQuery,
    tagLine,
    setTagLine,
    handleSearch,
    loading,
}: HeaderProps) => {
    const [time, setTime] = useState(new Date())

    useEffect(() => {
        const timer = setInterval(() => setTime(new Date()), 1000)
        return () => clearInterval(timer)
    }, [])

    return (
        <div className="border border-[#00FF00] mb-8">
            <div className="bg-[#00FF00] text-black px-4 py-2 flex items-center justify-between border-b border-[#00FF00]">
                <div className="flex items-center gap-2">
                    <Terminal className="w-4 h-4" />
                    <span className="font-bold">RASTREADOR_PARTIDAS.EXE</span>
                </div>
                <div className="text-xs">{time.toLocaleTimeString()}</div>
            </div>
            <div className="p-6">
                <div className="mb-4">
                    <span className="text-[#00FF00]">root@tracker:~$</span>{" "}
                    <span className="text-white">consulta --jogador</span>
                </div>
                <form onSubmit={handleSearch} className="relative">
                    <div className="flex items-center bg-black border border-[#00FF00] focus-within:border-[#00FFFF] focus-within:shadow-[0_0_10px_rgba(0,255,0,0.5)]">
                        <input
                            type="text"
                            placeholder="Nome de Invocador"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            disabled={loading}
                            className="w-full bg-transparent p-4 text-[#00FF00] font-mono placeholder:text-[#00FF00]/40 focus:outline-none"
                            autoComplete="off"
                        />
                        <span className="text-[#00FF00]/40">#</span>
                        <input
                            type="text"
                            placeholder="TAG"
                            value={tagLine}
                            onChange={(e) => setTagLine(e.target.value)}
                            disabled={loading}
                            className="w-24 bg-transparent p-4 text-[#00FF00] font-mono placeholder:text-[#00FF00]/40 focus:outline-none"
                            autoComplete="off"
                        />
                        <button
                            type="submit"
                            disabled={loading}
                            className="p-4"
                        >
                            <Search className="w-5 h-5 text-[#00FF00] hover:text-[#00FFFF] cursor-pointer" />
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}