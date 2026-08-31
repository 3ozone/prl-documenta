// @vitest-environment jsdom
import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import "@testing-library/jest-dom"
import type { AlertResponse } from "@/lib/types"
import { AlertBadge } from "@/components/alerts/AlertBadge"
import { AlertsClient } from "@/components/alerts/AlertsClient"

vi.mock("swr")
import useSWR from "swr"
const mockUseSWR = vi.mocked(useSWR)

beforeEach(() => {
  vi.clearAllMocks()
})

const makeAlert = (id: string, nivel: AlertResponse["nivel"], dias: number): AlertResponse => ({
  document_id: id,
  nombre_archivo: `doc_${id}.pdf`,
  categoria: "empresa",
  nivel,
  dias_restantes: dias,
})

describe("AlertBadge", () => {
  it("R5 — caducada → red classes", () => {
    render(<AlertBadge nivel="caducada" />)
    const badge = screen.getByText(/caducada/i)
    expect(badge.className).toContain("bg-red")
  })
  it("R5 — alerta_critica → orange classes", () => {
    render(<AlertBadge nivel="alerta_critica" />)
    const badge = screen.getByText(/alerta critica/i)
    expect(badge.className).toContain("bg-orange")
  })
  it("R5 — alerta → yellow classes", () => {
    render(<AlertBadge nivel="alerta" />)
    const badge = screen.getByText(/^alerta$/i)
    expect(badge.className).toContain("bg-yellow")
  })
  it("R5 — aviso → blue classes", () => {
    render(<AlertBadge nivel="aviso" />)
    const badge = screen.getByText(/aviso/i)
    expect(badge.className).toContain("bg-blue")
  })
})

const ALERTS = [
  makeAlert("3", "alerta", 30),
  makeAlert("1", "caducada", 5),
  makeAlert("2", "aviso", 60),
]

describe("AlertsClient", () => {
  it("R12 — shows loading state when isLoading=true", () => {
    mockUseSWR.mockReturnValue({ data: undefined, error: undefined, isLoading: true } as ReturnType<typeof useSWR>)
    render(<AlertsClient />)
    expect(screen.getByRole("status")).toBeInTheDocument()
  })

  it("R13 — shows error message on SWR error", () => {
    mockUseSWR.mockReturnValue({ data: undefined, error: new Error("fail"), isLoading: false } as ReturnType<typeof useSWR>)
    render(<AlertsClient />)
    expect(screen.getByText(/error al cargar/i)).toBeInTheDocument()
  })

  it("R6 — shows empty message when list is empty", () => {
    mockUseSWR.mockReturnValue({ data: [], error: undefined, isLoading: false } as ReturnType<typeof useSWR>)
    render(<AlertsClient />)
    expect(screen.getByText(/no hay alertas activas/i)).toBeInTheDocument()
  })

  it("R2 + R4 — renders alert list with all fields", () => {
    mockUseSWR.mockReturnValue({ data: ALERTS, error: undefined, isLoading: false } as ReturnType<typeof useSWR>)
    render(<AlertsClient />)
    expect(screen.getByText("doc_1.pdf")).toBeInTheDocument()
    expect(screen.getByText("doc_2.pdf")).toBeInTheDocument()
    expect(screen.getByText("doc_3.pdf")).toBeInTheDocument()
  })

  it("R2 — renders sorted by dias_restantes ascending", () => {
    mockUseSWR.mockReturnValue({ data: ALERTS, error: undefined, isLoading: false } as ReturnType<typeof useSWR>)
    render(<AlertsClient />)
    const rows = screen.getAllByRole("row")
    // header + 3 data rows; first data row should be caducada (dias=5)
    expect(rows[1]).toHaveTextContent("doc_1.pdf")
    expect(rows[2]).toHaveTextContent("doc_3.pdf")
    expect(rows[3]).toHaveTextContent("doc_2.pdf")
  })

  it("R9 — filter by nivel shows only matching alerts", async () => {
    mockUseSWR.mockReturnValue({ data: ALERTS, error: undefined, isLoading: false } as ReturnType<typeof useSWR>)
    render(<AlertsClient />)
    await userEvent.click(screen.getByRole("button", { name: /caducada/i }))
    expect(screen.getByText("doc_1.pdf")).toBeInTheDocument()
    expect(screen.queryByText("doc_2.pdf")).not.toBeInTheDocument()
    expect(screen.queryByText("doc_3.pdf")).not.toBeInTheDocument()
  })

  it("R10 — filter 'Todos' shows all alerts", async () => {
    mockUseSWR.mockReturnValue({ data: ALERTS, error: undefined, isLoading: false } as ReturnType<typeof useSWR>)
    render(<AlertsClient />)
    await userEvent.click(screen.getByRole("button", { name: /caducada/i }))
    await userEvent.click(screen.getByRole("button", { name: /todos/i }))
    expect(screen.getByText("doc_1.pdf")).toBeInTheDocument()
    expect(screen.getByText("doc_2.pdf")).toBeInTheDocument()
    expect(screen.getByText("doc_3.pdf")).toBeInTheDocument()
  })

  it("R7 — SWR is called with refreshInterval 60000", () => {
    mockUseSWR.mockReturnValue({ data: [], error: undefined, isLoading: false } as ReturnType<typeof useSWR>)
    render(<AlertsClient />)
    expect(mockUseSWR).toHaveBeenCalledWith(
      "/api/proxy/alerts",
      expect.any(Function),
      expect.objectContaining({ refreshInterval: 60000 })
    )
  })

  it("R11 — filter with no matches shows empty message", async () => {
    mockUseSWR.mockReturnValue({ data: ALERTS, error: undefined, isLoading: false } as ReturnType<typeof useSWR>)
    render(<AlertsClient />)
    await userEvent.click(screen.getByRole("button", { name: /alerta critica/i }))
    expect(screen.getByText(/no hay alertas activas/i)).toBeInTheDocument()
  })
})
