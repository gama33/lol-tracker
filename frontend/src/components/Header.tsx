import { Terminal } from "lucide-react"
import { useEffect, useState } from "react"

export const Header = () => {
    const [time, setTime] = useState(new Date())

    useEffect(() => {
        const timer = setInterval(() => setTime(new Date()), 1000)
        return () => clearInterval(timer)
    }, [])

    return (
        <div className="border border-[#00FF00] mb-8">
            <div className="bg-[#00FF00] text-black px-4 py-2 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <Terminal className="w-4 h-4" />
                    <span className="font-bold">RASTREADOR_PARTIDAS.EXE</span>
                </div>
                <div className="text-xs">{time.toLocaleTimeString()}</div>
            </div>
        </div>
    )
}
