"use client"

import useSWR from "swr"
import { useState } from "react"
import type { AlertResponse } from "@/lib/types"
import { AlertsTable } from "./AlertsTable"

const fetcher = (url: string) => fetch(url).then((r) => r.json())

const NIVELES = ["todos", "caducada", "alerta_critica", "alerta", "aviso"] as const
type NivelFiltro = typeof NIVELES[number]

const AlertsClient = () => {
  const [nivelFiltro, setNivelFiltro] = useState<NivelFiltro>("todos")
  const { data, error, isLoading } = useSWR<AlertResponse[]>(
    "/api/proxy/alerts",
    fetcher,
    { refreshInterval: 60000 }
  )

  if (isLoading) {
    return <div role="status" aria-label="Cargando alertas" className="h-24 animate-pulse rounded bg-gray-200" />
  }
  if (error) {
    return <p className="text-red-600">Error al cargar las alertas.</p>
  }

  const sorted = [...(data ?? [])].sort((a, b) => a.dias_restantes - b.dias_restantes)
  const filtered = nivelFiltro === "todos" ? sorted : sorted.filter((a) => a.nivel === nivelFiltro)

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap gap-2">
        {NIVELES.map((nivel) => (
          <button
            key={nivel}
            onClick={() => setNivelFiltro(nivel)}
            className={`rounded px-3 py-1 text-sm ${nivelFiltro === nivel ? "bg-blue-600 text-white" : "bg-gray-100 text-gray-700 hover:bg-gray-200"}`}
            aria-pressed={nivelFiltro === nivel}
          >
            {nivel === "todos" ? "Todos" : nivel.replace(/_/g, " ")}
          </button>
        ))}
      </div>
      {filtered.length === 0 ? (
        <p>No hay alertas activas.</p>
      ) : (
        <AlertsTable alerts={filtered} />
      )}
    </div>
  )
}

export { AlertsClient }
