export const formatKDA = (abates: number, mortes: number, assistencias: number) => {
    return `${abates}/${mortes}/${assistencias}`
}

export const formatTimeAgo = (timestamp: number) => {
    const diff = Date.now() - timestamp
    const hours = Math.floor(diff / (1000 * 60 * 60))
    const days = Math.floor(hours / 24)

    if (days > 0) return `${days}d ago`
    if (hours > 0) return `${hours}h ago`
    return 'now'
}
