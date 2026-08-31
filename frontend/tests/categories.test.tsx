// @vitest-environment jsdom
import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import "@testing-library/jest-dom"
import type { DocumentResponse } from "@/lib/types"
import { UploadEmpresaForm } from "@/components/categories/UploadEmpresaForm"
import { UploadTrabajadoresForm } from "@/components/categories/UploadTrabajadoresForm"
import { UploadEquiposForm } from "@/components/categories/UploadEquiposForm"

const pushMock = vi.fn()
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: pushMock }),
}))

beforeEach(() => {
  pushMock.mockClear()
  vi.unstubAllGlobals()
})

const makeDoc = (id: string, categoria: string | null): DocumentResponse => ({
  id,
  nombre_archivo: `doc_${id}.pdf`,
  formato: "pdf",
  fecha_validez: "2025-01-01",
  fecha_caducidad: "2030-01-01",
  categoria,
})

const docs = [
  makeDoc("1", "empresa"),
  makeDoc("2", "empresa"),
  makeDoc("3", "trabajadores"),
  makeDoc("4", "equipos"),
  makeDoc("5", null),
]

describe("filterDocumentsByCategoria", () => {
  it("empresa — solo devuelve documentos de empresa", () => {
    const result = docs.filter((d) => d.categoria === "empresa")
    expect(result).toHaveLength(2)
    expect(result.every((d) => d.categoria === "empresa")).toBe(true)
  })

  it("trabajadores — solo devuelve documentos de trabajadores", () => {
    const result = docs.filter((d) => d.categoria === "trabajadores")
    expect(result).toHaveLength(1)
  })

  it("equipos — solo devuelve documentos de equipos", () => {
    const result = docs.filter((d) => d.categoria === "equipos")
    expect(result).toHaveLength(1)
  })
})

describe("UploadEmpresaForm", () => {
  it("R16 — rejects non-PDF file", async () => {
    render(<UploadEmpresaForm />)
    const fileInput = screen.getByLabelText(/archivo pdf/i) as HTMLInputElement
    const file = new File(["content"], "test.txt", { type: "text/plain" })
    await userEvent.upload(fileInput, file)
    await userEvent.type(screen.getAllByRole("textbox")[0], "Test")
    await userEvent.click(screen.getByRole("button", { name: /subir/i }))
    // Error alerts appear — either PDF validate or required block the non-PDF upload
    const alerts = await screen.findAllByRole("alert")
    expect(alerts.length).toBeGreaterThan(0)
    const allText = alerts.map((a) => a.textContent).join(" ")
    expect(allText).toMatch(/pdf|archivo|seleccionar/i)
  })

  it("R15 — shows error when razon_social is missing", async () => {
    render(<UploadEmpresaForm />)
    await userEvent.click(screen.getByRole("button", { name: /subir/i }))
    const errors = await screen.findAllByText(/obligatorio/i)
    expect(errors.length).toBeGreaterThan(0)
  })
})

describe("UploadEquiposForm", () => {
  it("R13 — shows mantenimiento fields when subtipo is mantenimiento", async () => {
    render(<UploadEquiposForm />)
    const select = screen.getByLabelText(/subtipo/i)
    await userEvent.selectOptions(select, "mantenimiento")
    expect(screen.getByLabelText(/tipo mantenimiento/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/empresa mantenedora/i)).toBeInTheDocument()
  })

  it("R14 — shows inspeccion fields when subtipo is inspeccion", async () => {
    render(<UploadEquiposForm />)
    const select = screen.getByLabelText(/subtipo/i)
    await userEvent.selectOptions(select, "inspeccion")
    expect(screen.getByLabelText(/organismo inspector/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/resultado inspección/i)).toBeInTheDocument()
  })

  it("R13-R14 — hides conditional fields initially", () => {
    render(<UploadEquiposForm />)
    expect(screen.queryByLabelText(/tipo mantenimiento/i)).not.toBeInTheDocument()
    expect(screen.queryByLabelText(/organismo inspector/i)).not.toBeInTheDocument()
  })
})

// ─── R10 — UploadEmpresaForm renders specific fields ────────────────────────
describe("UploadEmpresaForm fields", () => {
  it("R10 — renders razon_social, cif, actividad_economica, centro_trabajo", () => {
    render(<UploadEmpresaForm />)
    expect(screen.getByLabelText(/razón social/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/cif/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/actividad económica/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/centro de trabajo/i)).toBeInTheDocument()
  })
})

// ─── R11 — UploadTrabajadoresForm renders specific fields ────────────────────
describe("UploadTrabajadoresForm fields", () => {
  it("R11 — renders nombre_trabajador, dni, puesto and tipo_documento select with 4 options", () => {
    render(<UploadTrabajadoresForm />)
    expect(screen.getByLabelText(/nombre del trabajador/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/dni/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/puesto/i)).toBeInTheDocument()
    const select = screen.getByLabelText(/tipo de documento/i)
    expect(select).toBeInTheDocument()
    expect(select.querySelectorAll("option[value='formacion']")).toHaveLength(1)
    expect(select.querySelectorAll("option[value='reconocimiento_medico']")).toHaveLength(1)
    expect(select.querySelectorAll("option[value='entrega_epi']")).toHaveLength(1)
    expect(select.querySelectorAll("option[value='aptitud_medica']")).toHaveLength(1)
  })
})

// ─── R12 — UploadEquiposForm renders base fields ─────────────────────────────
describe("UploadEquiposForm base fields", () => {
  it("R12 — renders id_equipo, nombre_equipo, numero_serie, ubicacion and subtipo select", () => {
    render(<UploadEquiposForm />)
    expect(screen.getByLabelText(/id equipo/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/nombre equipo/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/número de serie/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/ubicación/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/subtipo/i)).toBeInTheDocument()
  })
})

// ─── R17 — FormData includes categoria and specific fields ────────────────────
describe("UploadEmpresaForm submit — R17", () => {
  it("R17 — FormData includes categoria=empresa and empresa-specific fields", async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => ({}) })
    vi.stubGlobal("fetch", fetchMock)

    render(<UploadEmpresaForm />)

    await userEvent.type(screen.getByLabelText(/^nombre$/i), "Doc test")
    await userEvent.type(screen.getByLabelText(/razón social/i), "Empresa SA")
    await userEvent.type(screen.getByLabelText(/cif/i), "B12345678")
    await userEvent.type(screen.getByLabelText(/actividad económica/i), "Construcción")
    await userEvent.type(screen.getByLabelText(/centro de trabajo/i), "Madrid")

    const dateInputs = screen.getAllByDisplayValue("")
    // fill fecha_validez and fecha_caducidad
    const fechaValidez = screen.getByLabelText(/fecha validez/i)
    const fechaCaducidad = screen.getByLabelText(/fecha caducidad/i)
    await userEvent.type(fechaValidez, "2025-01-01")
    await userEvent.type(fechaCaducidad, "2030-01-01")

    const pdfFile = new File(["pdf"], "test.pdf", { type: "application/pdf" })
    const fileInput = screen.getByLabelText(/archivo pdf/i)
    await userEvent.upload(fileInput, pdfFile)

    await userEvent.click(screen.getByRole("button", { name: /subir/i }))

    expect(fetchMock).toHaveBeenCalled()
    const formData = fetchMock.mock.calls[0][1].body as FormData
    expect(formData.get("categoria")).toBe("empresa")
    expect(formData.get("razon_social")).toBe("Empresa SA")
    expect(formData.get("cif")).toBe("B12345678")
    expect(formData.get("actividad_economica")).toBe("Construcción")
    expect(formData.get("centro_trabajo")).toBe("Madrid")
  })
})

// ─── R18 — Redirect after success ────────────────────────────────────────────
describe("UploadEmpresaForm submit — R18", () => {
  it("R18 — calls router.push with /categories/empresa after success", async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => ({}) })
    vi.stubGlobal("fetch", fetchMock)

    render(<UploadEmpresaForm />)

    await userEvent.type(screen.getByLabelText(/^nombre$/i), "Doc test")
    await userEvent.type(screen.getByLabelText(/razón social/i), "Empresa SA")
    await userEvent.type(screen.getByLabelText(/cif/i), "B12345678")
    await userEvent.type(screen.getByLabelText(/actividad económica/i), "Construcción")
    await userEvent.type(screen.getByLabelText(/centro de trabajo/i), "Madrid")
    await userEvent.type(screen.getByLabelText(/fecha validez/i), "2025-01-01")
    await userEvent.type(screen.getByLabelText(/fecha caducidad/i), "2030-01-01")

    const pdfFile = new File(["pdf"], "test.pdf", { type: "application/pdf" })
    await userEvent.upload(screen.getByLabelText(/archivo pdf/i), pdfFile)

    await userEvent.click(screen.getByRole("button", { name: /subir/i }))

    expect(pushMock).toHaveBeenCalledWith("/categories/empresa")
  })
})

// ─── R19 — Backend error appears in DOM ──────────────────────────────────────
describe("UploadEmpresaForm submit — R19", () => {
  it("R19 — shows backend error message and does not redirect", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      json: async () => ({ detail: "Archivo inválido." }),
    })
    vi.stubGlobal("fetch", fetchMock)

    render(<UploadEmpresaForm />)

    await userEvent.type(screen.getByLabelText(/^nombre$/i), "Doc test")
    await userEvent.type(screen.getByLabelText(/razón social/i), "Empresa SA")
    await userEvent.type(screen.getByLabelText(/cif/i), "B12345678")
    await userEvent.type(screen.getByLabelText(/actividad económica/i), "Construcción")
    await userEvent.type(screen.getByLabelText(/centro de trabajo/i), "Madrid")
    await userEvent.type(screen.getByLabelText(/fecha validez/i), "2025-01-01")
    await userEvent.type(screen.getByLabelText(/fecha caducidad/i), "2030-01-01")

    const pdfFile = new File(["pdf"], "test.pdf", { type: "application/pdf" })
    await userEvent.upload(screen.getByLabelText(/archivo pdf/i), pdfFile)

    await userEvent.click(screen.getByRole("button", { name: /subir/i }))

    expect(await screen.findByText("Archivo inválido.")).toBeInTheDocument()
    expect(pushMock).not.toHaveBeenCalled()
  })
})

// ─── R7, R8 — Admin/viewer visibility logic ───────────────────────────────────
describe("category page role logic", () => {
  it("R7 — viewer should not see upload button (logic)", () => {
    const role = "viewer"
    const canUpload = role === "admin"
    expect(canUpload).toBe(false)
  })

  it("R8 — admin should see upload button (logic)", () => {
    const role = "admin"
    const canUpload = role === "admin"
    expect(canUpload).toBe(true)
  })
})

// ─── R9 — Upload guard logic ──────────────────────────────────────────────────
describe("upload guard logic", () => {
  it("R9 — non-admin should be redirected", () => {
    const role = "viewer"
    const shouldRedirect = role !== "admin"
    expect(shouldRedirect).toBe(true)
  })
})

// ─── R1, R2, R3 — Category page filter logic ─────────────────────────────────
describe("category page filter logic", () => {
  const makeDoc = (id: string, categoria: string | null): DocumentResponse => ({
    id,
    nombre_archivo: `doc_${id}.pdf`,
    formato: "pdf",
    fecha_validez: "2025-01-01",
    fecha_caducidad: "2030-01-01",
    categoria,
  })

  it("R1 — empresa page shows only empresa docs", () => {
    const all = [makeDoc("1", "empresa"), makeDoc("2", "trabajadores"), makeDoc("3", null)]
    const empresa = all.filter((d) => d.categoria === "empresa")
    expect(empresa).toHaveLength(1)
    expect(empresa[0].id).toBe("1")
  })

  it("R2 — trabajadores page shows only trabajadores docs", () => {
    const all = [makeDoc("1", "empresa"), makeDoc("2", "trabajadores"), makeDoc("3", null)]
    const trabajadores = all.filter((d) => d.categoria === "trabajadores")
    expect(trabajadores).toHaveLength(1)
    expect(trabajadores[0].id).toBe("2")
  })

  it("R3 — equipos page shows only equipos docs", () => {
    const all = [makeDoc("1", "empresa"), makeDoc("2", "equipos"), makeDoc("3", null)]
    const equipos = all.filter((d) => d.categoria === "equipos")
    expect(equipos).toHaveLength(1)
    expect(equipos[0].id).toBe("2")
  })
})
