import { describe, it, expect, vi } from "vitest"

vi.mock("next/headers", () => ({
  cookies: vi.fn(),
}))

import { cookies } from "next/headers"
import { GET } from "@/app/api/proxy/documents/[id]/download/route"
import type { NextRequest } from "next/server"

const mockParams = (id: string) => Promise.resolve({ id })

describe("GET /api/proxy/documents/[id]/download route handler", () => {
  it("R15 — returns application/pdf content-type on success", async () => {
    vi.mocked(cookies).mockResolvedValue({
      get: (name: string) => name === "token" ? { value: "tok" } : undefined,
    } as any)

    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      body: new ReadableStream(),
    }))

    const res = await GET({} as NextRequest, { params: mockParams("123") })
    expect(res.headers.get("Content-Type")).toBe("application/pdf")
    vi.unstubAllGlobals()
    vi.clearAllMocks()
  })

  it("R16 — returns 404 with 'Documento no encontrado' when backend returns 404", async () => {
    vi.mocked(cookies).mockResolvedValue({
      get: (name: string) => name === "token" ? { value: "tok" } : undefined,
    } as any)

    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: false,
      status: 404,
    }))

    const res = await GET({} as NextRequest, { params: mockParams("999") })
    expect(res.status).toBe(404)
    const body = await res.text()
    expect(body).toBe("Documento no encontrado")
    vi.unstubAllGlobals()
    vi.clearAllMocks()
  })
})
