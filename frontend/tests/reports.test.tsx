// @vitest-environment jsdom
import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen, fireEvent, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import "@testing-library/jest-dom"
import { ReportsForm } from "@/app/reports/ReportsForm"

// Mock URL methods
const createObjectURLMock = vi.fn(() => "blob:http://localhost/mock")
const revokeObjectURLMock = vi.fn()
vi.stubGlobal("URL", { createObjectURL: createObjectURLMock, revokeObjectURL: revokeObjectURLMock })

const fetchMock = vi.fn()

beforeEach(() => {
  vi.stubGlobal("fetch", fetchMock)
  fetchMock.mockClear()
  createObjectURLMock.mockClear()
  revokeObjectURLMock.mockClear()
})

describe("ReportsForm", () => {
  it("R3 — default format is CSV", () => {
    render(<ReportsForm />)
    const select = screen.getByLabelText(/formato/i) as HTMLSelectElement
    expect(select.value).toBe("csv")
  })

  it("R4 — default category is 'todas'", () => {
    render(<ReportsForm />)
    const select = screen.getByLabelText(/categoría/i) as HTMLSelectElement
    expect(select.value).toBe("todas")
  })

  it("R3 — has both CSV and PDF options", () => {
    render(<ReportsForm />)
    expect(screen.getByRole("option", { name: /csv/i })).toBeInTheDocument()
    expect(screen.getByRole("option", { name: /pdf/i })).toBeInTheDocument()
  })

  it("R4 — has all 4 category options", () => {
    render(<ReportsForm />)
    expect(screen.getByRole("option", { name: /todas/i })).toBeInTheDocument()
    expect(screen.getByRole("option", { name: /empresa/i })).toBeInTheDocument()
    expect(screen.getByRole("option", { name: /trabajadores/i })).toBeInTheDocument()
    expect(screen.getByRole("option", { name: /equipos/i })).toBeInTheDocument()
  })

  it("R5 — button is disabled while loading", async () => {
    let resolveFetch: (v: unknown) => void
    fetchMock.mockReturnValue(new Promise((r) => { resolveFetch = r }))
    render(<ReportsForm />)
    const button = screen.getByRole("button", { name: /generar informe/i })
    fireEvent.click(button)
    await waitFor(() => expect(button).toBeDisabled())
    resolveFetch!({ ok: true, status: 200, blob: async () => new Blob(["data"], { type: "text/csv" }) })
  })

  it("R9/R10 — on success, createObjectURL is called and button re-enabled", async () => {
    fetchMock.mockResolvedValue({
      ok: true,
      status: 200,
      blob: async () => new Blob(["data"], { type: "text/csv" }),
    })
    render(<ReportsForm />)
    const button = screen.getByRole("button", { name: /generar informe/i })
    await userEvent.click(button)
    await waitFor(() => expect(button).not.toBeDisabled())
    expect(createObjectURLMock).toHaveBeenCalled()
    expect(revokeObjectURLMock).toHaveBeenCalled()
  })

  it("R11 — shows permission error on 401", async () => {
    fetchMock.mockResolvedValue({ ok: false, status: 401 })
    render(<ReportsForm />)
    await userEvent.click(screen.getByRole("button", { name: /generar informe/i }))
    expect(await screen.findByText(/no tienes permiso/i)).toBeInTheDocument()
  })

  it("R12 — shows generic error on 500", async () => {
    fetchMock.mockResolvedValue({ ok: false, status: 500 })
    render(<ReportsForm />)
    await userEvent.click(screen.getByRole("button", { name: /generar informe/i }))
    expect(await screen.findByText(/error al generar el informe/i)).toBeInTheDocument()
  })
})
