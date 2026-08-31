// @vitest-environment jsdom
import { describe, it, expect } from "vitest"
import { render, screen } from "@testing-library/react"
import "@testing-library/jest-dom"
import { DocumentsTable } from "@/components/documents/DocumentsTable"
import type { DocumentResponse } from "@/lib/types"

const makeDoc = (id: string, fecha_caducidad = "2030-01-01"): DocumentResponse => ({
  id,
  nombre_archivo: `doc_${id}.pdf`,
  formato: "pdf",
  fecha_validez: "2025-01-01",
  fecha_caducidad,
  categoria: null,
})

describe("DocumentsTable", () => {
  it("R2 — renders all column headers", () => {
    render(<DocumentsTable docs={[]} page={1} />)
    expect(screen.getByText(/nombre/i)).toBeInTheDocument()
    expect(screen.getByText(/fecha validez/i)).toBeInTheDocument()
    expect(screen.getByText(/fecha caducidad/i)).toBeInTheDocument()
    expect(screen.getByText(/estado/i)).toBeInTheDocument()
    expect(screen.getByText(/acciones/i)).toBeInTheDocument()
  })

  it("R2 — renders document row with download link", () => {
    render(<DocumentsTable docs={[makeDoc("1")]} page={1} />)
    expect(screen.getByText("doc_1.pdf")).toBeInTheDocument()
    expect(screen.getByRole("link", { name: /descargar/i })).toBeInTheDocument()
  })

  it("R1 — shows vigente badge for future document", () => {
    render(<DocumentsTable docs={[makeDoc("1", "2030-01-01")]} page={1} />)
    expect(screen.getByText("Vigente")).toBeInTheDocument()
  })

  it("R1 — shows caducada badge for expired document", () => {
    render(<DocumentsTable docs={[makeDoc("1", "2020-01-01")]} page={1} />)
    expect(screen.getByText("Caducada")).toBeInTheDocument()
  })

  it("R2 — shows empty state when no documents", () => {
    render(<DocumentsTable docs={[]} page={1} />)
    expect(screen.getByText(/no hay documentos/i)).toBeInTheDocument()
  })
})
