import { getAlerts } from "@/lib/api"
import log from "@/lib/logger"
import type { AlertLevel } from "@/lib/types"

const ALERT_LEVELS: AlertLevel[] = ["aviso", "alerta", "alerta_critica", "caducada"]

const LEVEL_LABELS: Record<AlertLevel, string> = {
  aviso: "Aviso",
  alerta: "Alerta",
  alerta_critica: "Alerta crítica",
  caducada: "Caducada",
}

const LEVEL_COLORS: Record<AlertLevel, string> = {
  aviso: "text-blue-700 bg-blue-50",
  alerta: "text-yellow-700 bg-yellow-50",
  alerta_critica: "text-orange-700 bg-orange-50",
  caducada: "text-red-700 bg-red-50",
}

const AlertSummaryWidget = async ({ token }: { token: string }) => {
  const counts: Record<AlertLevel, number> = {
    aviso: 0, alerta: 0, alerta_critica: 0, caducada: 0,
  }

  try {
    const alerts = await getAlerts(token)
    for (const alert of alerts) {
      if (alert.nivel in counts) counts[alert.nivel as AlertLevel]++
    }
  } catch (err) {
    log.error({ err: String(err) }, "dashboard.alerts.fetch_failed")
    return (
      <div className="rounded border p-4 text-red-600">
        No se pudieron cargar las alertas.
      </div>
    )
  }

  return (
    <section className="rounded border p-4">
      <h2 className="text-lg font-semibold mb-3">Alertas por nivel</h2>
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
        {ALERT_LEVELS.map((level) => (
          <div key={level} className={`rounded p-3 text-center ${LEVEL_COLORS[level]}`}>
            <p className="text-2xl font-bold">{counts[level]}</p>
            <p className="text-sm">{LEVEL_LABELS[level]}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

export { AlertSummaryWidget }
