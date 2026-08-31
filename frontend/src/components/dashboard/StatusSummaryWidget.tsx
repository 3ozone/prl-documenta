import { getDocuments } from "@/lib/api"
import log from "@/lib/logger"
import type { DocumentStatus } from "@/lib/types"

const EXPIRY_WARNING_DAYS = 30

export const classifyStatus = (fechaCaducidad: string): DocumentStatus => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const expiry = new Date(fechaCaducidad)
  expiry.setHours(0, 0, 0, 0)
  const diffMs = expiry.getTime() - today.getTime()
  const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24))
  if (diffDays < 0) return "caducada"
  if (diffDays <= EXPIRY_WARNING_DAYS) return "proxima_a_caducar"
  return "vigente"
}

const STATUS_LABELS: Record<DocumentStatus, string> = {
  vigente: "Vigente",
  proxima_a_caducar: "Próxima a caducar",
  caducada: "Caducada",
}

const STATUS_COLORS: Record<DocumentStatus, string> = {
  vigente: "text-green-700 bg-green-50",
  proxima_a_caducar: "text-yellow-700 bg-yellow-50",
  caducada: "text-red-700 bg-red-50",
}

const STATUSES: DocumentStatus[] = ["vigente", "proxima_a_caducar", "caducada"]

const StatusSummaryWidget = async ({ token }: { token: string }) => {
  const counts: Record<DocumentStatus, number> = {
    vigente: 0, proxima_a_caducar: 0, caducada: 0,
  }

  try {
    const docs = await getDocuments(token)
    for (const doc of docs) {
      const status = classifyStatus(doc.fecha_caducidad)
      counts[status]++
    }
  } catch (err) {
    log.error({ err: String(err) }, "dashboard.status.fetch_failed")
    return (
      <div className="rounded border p-4 text-red-600">
        No se pudieron cargar los documentos por estado.
      </div>
    )
  }

  return (
    <section className="rounded border p-4">
      <h2 className="text-lg font-semibold mb-3">Documentos por estado</h2>
      <div className="grid grid-cols-3 gap-2">
        {STATUSES.map((status) => (
          <div key={status} className={`rounded p-3 text-center ${STATUS_COLORS[status]}`}>
            <p className="text-2xl font-bold">{counts[status]}</p>
            <p className="text-sm">{STATUS_LABELS[status]}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

export { StatusSummaryWidget }
