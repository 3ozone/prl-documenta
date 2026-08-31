import { describe, it, expect } from "vitest"
import { classifyStatus } from "@/lib/classifyStatus"
import type { DocumentResponse } from "@/lib/types"

const doc = (fecha_caducidad: string): DocumentResponse => ({
  id: "1",
  nombre_archivo: "test.pdf",
  formato: "pdf",
  fecha_validez: "2025-01-01",
  fecha_caducidad,
  categoria: null,
})

describe("classifyStatus", () => {
  it("returns caducada when expiry date is past", () => {
    expect(classifyStatus(doc("2020-01-01"), "2026-01-15")).toBe("caducada")
  })

  it("returns proxima_a_caducar when expiry is exactly 30 days away", () => {
    expect(classifyStatus(doc("2026-02-14"), "2026-01-15")).toBe("proxima_a_caducar")
  })

  it("returns proxima_a_caducar when expiry is less than 30 days away", () => {
    expect(classifyStatus(doc("2026-01-25"), "2026-01-15")).toBe("proxima_a_caducar")
  })

  it("returns vigente when expiry is more than 30 days away", () => {
    expect(classifyStatus(doc("2026-03-01"), "2026-01-15")).toBe("vigente")
  })
})
