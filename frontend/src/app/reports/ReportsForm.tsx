"use client"

import { useState } from "react"
import type { ReportFormat, ReportCategoria } from "@/lib/types"
import log from "@/lib/logger"

const ReportsForm = () => {
  const [formato, setFormato] = useState<ReportFormat>("csv")
  const [categoria, setCategoria] = useState<ReportCategoria>("todas")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`/api/proxy/reports?formato=${formato}&categoria=${categoria}`)
      if (res.status === 401 || res.status === 403) {
        setError("No tienes permiso para generar informes.")
        return
      }
      if (!res.ok) {
        setError("Error al generar el informe. Inténtalo de nuevo.")
        return
      }
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `informe.${formato}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (err) {
      log.error({ err: String(err) }, "reports.generate_failed")
      setError("Error al generar el informe. Inténtalo de nuevo.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col gap-4 max-w-sm">
      <div>
        <label htmlFor="formato" className="block text-sm font-medium">Formato</label>
        <select
          id="formato"
          value={formato}
          onChange={(e) => setFormato(e.target.value as ReportFormat)}
          className="mt-1 w-full border rounded px-3 py-2"
        >
          <option value="csv">CSV</option>
          <option value="pdf">PDF</option>
        </select>
      </div>
      <div>
        <label htmlFor="categoria" className="block text-sm font-medium">Categoría</label>
        <select
          id="categoria"
          value={categoria}
          onChange={(e) => setCategoria(e.target.value as ReportCategoria)}
          className="mt-1 w-full border rounded px-3 py-2"
        >
          <option value="todas">Todas</option>
          <option value="empresa">Empresa</option>
          <option value="trabajadores">Trabajadores</option>
          <option value="equipos">Equipos</option>
        </select>
      </div>
      <button
        onClick={handleGenerate}
        disabled={loading}
        className="bg-blue-600 text-white rounded px-4 py-2 disabled:opacity-50"
      >
        {loading ? "Generando…" : "Generar informe"}
      </button>
      {error && <p role="alert" className="text-red-600 text-sm">{error}</p>}
    </div>
  )
}

export { ReportsForm }
