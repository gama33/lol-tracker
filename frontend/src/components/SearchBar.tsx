import { Search } from "lucide-react"

interface SearchBarProps {
    searchQuery: string
    setSearchQuery: (query: string) => void
    handleSearch: () => void
    loading: boolean
}

export const SearchBar = ({ searchQuery, setSearchQuery, handleSearch, loading }: SearchBarProps) => {
    return (
        <div className="p-6 border border-[#00FF00] mb-8">
            <div className="mb-4">
                <span className="text-[#00FF00]">root@tracker:~$</span>{" "}
                <span className="text-white">consulta --jogador</span>
            </div>
            <div className="relative">
                <input
                    type="text"
                    placeholder="Digite o nome de invocador..."
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
    )
}
