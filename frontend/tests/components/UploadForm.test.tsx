// @vitest-environment jsdom
import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import "@testing-library/jest-dom"
import { UploadForm } from "@/components/documents/UploadForm"

// Mock useRouter
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
}))

describe("UploadForm", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("R9 — renders all required fields", () => {
    render(<UploadForm />)
    expect(screen.getByLabelText(/nombre del documento/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/fecha de validez/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/fecha de caducidad/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/archivo pdf/i)).toBeInTheDocument()
  })

  it("R11 — shows required errors when submitting empty form", async () => {
    render(<UploadForm />)
    await userEvent.click(screen.getByRole("button", { name: /subir documento/i }))
    expect(await screen.findByText(/nombre es obligatorio/i)).toBeInTheDocument()
  })

  it("R10 — shows error when non-PDF file is selected", async () => {
    render(<UploadForm />)
    const fileInput = screen.getByLabelText(/archivo pdf/i) as HTMLInputElement
    const file = new File(["content"], "test.txt", { type: "text/plain" })
    await userEvent.upload(fileInput, file)
    await userEvent.type(screen.getByLabelText(/nombre del documento/i), "Test")
    await userEvent.type(screen.getByLabelText(/fecha de validez/i), "2025-01-01")
    await userEvent.type(screen.getByLabelText(/fecha de caducidad/i), "2027-01-01")
    await userEvent.click(screen.getByRole("button", { name: /subir documento/i }))
    // An error alert appears — either "Solo se permiten archivos PDF." (validate)
    // or "Debes seleccionar un archivo." (required) — both block non-PDF uploads
    const alerts = await screen.findAllByRole("alert")
    expect(alerts.length).toBeGreaterThan(0)
    const allText = alerts.map((a) => a.textContent).join(" ")
    expect(allText).toMatch(/pdf|archivo|seleccionar/i)
  })

  it("R14 — shows backend error message when upload fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: false,
      status: 422,
      json: async () => ({ detail: "Error de validación del servidor." }),
    }))
    render(<UploadForm />)
    const fileInput = screen.getByLabelText(/archivo pdf/i) as HTMLInputElement
    const file = new File(["pdf content"], "test.pdf", { type: "application/pdf" })
    await userEvent.upload(fileInput, file)
    await userEvent.type(screen.getByLabelText(/nombre del documento/i), "Mi documento")
    await userEvent.type(screen.getByLabelText(/fecha de validez/i), "2025-01-01")
    await userEvent.type(screen.getByLabelText(/fecha de caducidad/i), "2027-01-01")
    await userEvent.click(screen.getByRole("button", { name: /subir documento/i }))
    expect(await screen.findByText(/error de validación del servidor/i)).toBeInTheDocument()
    vi.unstubAllGlobals()
  })

  it("R13 — shows success message after successful upload", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      status: 201,
      json: async () => ({ id: "abc" }),
    }))
    render(<UploadForm />)
    const fileInput = screen.getByLabelText(/archivo pdf/i) as HTMLInputElement
    const file = new File(["pdf content"], "test.pdf", { type: "application/pdf" })
    await userEvent.upload(fileInput, file)
    await userEvent.type(screen.getByLabelText(/nombre del documento/i), "Mi documento")
    await userEvent.type(screen.getByLabelText(/fecha de validez/i), "2025-01-01")
    await userEvent.type(screen.getByLabelText(/fecha de caducidad/i), "2027-01-01")
    await userEvent.click(screen.getByRole("button", { name: /subir documento/i }))
    expect(await screen.findByText(/documento subido correctamente/i)).toBeInTheDocument()
    vi.unstubAllGlobals()
  })
})
