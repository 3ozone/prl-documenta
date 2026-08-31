import { describe, it, expect } from "vitest"
import { classifyStatus } from "@/components/dashboard/StatusSummaryWidget"

// Helper para agrupar alertas
const groupAlertsByLevel = (alerts: Array<{ nivel: string }>) => {
  const counts: Record<string, number> = { aviso: 0, alerta: 0, alerta_critica: 0, caducada: 0 }
  for (const a of alerts) {
    if (a.nivel in counts) counts[a.nivel]++
  }
  return counts
}

// Helper para agrupar documentos por categoría
const groupDocsByCategory = (docs: Array<{ categoria: string | null }>) => {
  const counts = { empresa: 0, trabajadores: 0, equipos: 0 }
  for (const d of docs) {
    if (d.categoria === "empresa") counts.empresa++
    else if (d.categoria === "trabajadores") counts.trabajadores++
    else if (d.categoria === "equipos") counts.equipos++
  }
  return counts
}

describe("groupAlertsByLevel", () => {
  it("groups alerts by level and initialises missing levels to 0", () => {
    const alerts = [
      { nivel: "aviso" },
      { nivel: "aviso" },
      { nivel: "alerta_critica" },
    ]
    const result = groupAlertsByLevel(alerts)
    expect(result.aviso).toBe(2)
    expect(result.alerta).toBe(0)
    expect(result.alerta_critica).toBe(1)
    expect(result.caducada).toBe(0)
  })
})

describe("groupDocsByCategory", () => {
  it("groups documents by category and initialises missing categories to 0", () => {
    const docs = [
      { categoria: "empresa" },
      { categoria: "empresa" },
      { categoria: "trabajadores" },
      { categoria: null },
    ]
    const result = groupDocsByCategory(docs)
    expect(result.empresa).toBe(2)
    expect(result.trabajadores).toBe(1)
    expect(result.equipos).toBe(0)
  })
})

describe("classifyStatus", () => {
  it("classifies as vigente when expiry > 30 days", () => {
    const future = new Date()
    future.setDate(future.getDate() + 60)
    expect(classifyStatus(future.toISOString().split("T")[0])).toBe("vigente")
  })

  it("classifies as proxima_a_caducar when expiry <= 30 days", () => {
    const soon = new Date()
    soon.setDate(soon.getDate() + 15)
    expect(classifyStatus(soon.toISOString().split("T")[0])).toBe("proxima_a_caducar")
  })

  it("classifies as caducada when expiry date is past", () => {
    const past = new Date()
    past.setDate(past.getDate() - 5)
    expect(classifyStatus(past.toISOString().split("T")[0])).toBe("caducada")
  })
})
