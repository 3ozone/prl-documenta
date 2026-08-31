// @vitest-environment node
import { describe, it, expect, vi, beforeEach } from "vitest"
import { NextRequest } from "next/server"

// Mock fetch
const fetchMock = vi.fn()
vi.stubGlobal("fetch", fetchMock)

import { GET } from "@/app/api/proxy/reports/route"

const makeReq = (token?: string, formato = "csv", categoria = "todas") => {
  const headers: HeadersInit = token ? { cookie: `token=${token}` } : {}
  return new NextRequest(
    `http://localhost/api/proxy/reports?formato=${formato}&categoria=${categoria}`,
    { headers }
  )
}

beforeEach(() => {
  fetchMock.mockClear()
})

describe("GET /api/proxy/reports", () => {
  it("R7/R11 — returns 401 when no token", async () => {
    const res = await GET(makeReq(undefined))
    expect(res.status).toBe(401)
  })

  it("R8 — returns blob with correct headers on 200", async () => {
    const buffer = new ArrayBuffer(8)
    fetchMock.mockResolvedValue({
      ok: true,
      status: 200,
      arrayBuffer: async () => buffer,
      headers: new Headers({
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=informe.csv",
      }),
    })
    const res = await GET(makeReq("tok123"))
    expect(res.status).toBe(200)
    expect(res.headers.get("Content-Type")).toBe("text/csv")
  })

  it("R11 — returns 403 when backend responds 403", async () => {
    fetchMock.mockResolvedValue({ ok: false, status: 403 })
    const res = await GET(makeReq("tok123"))
    expect(res.status).toBe(403)
  })

  it("R12 — returns 502 when backend responds 500", async () => {
    fetchMock.mockResolvedValue({ ok: false, status: 500 })
    const res = await GET(makeReq("tok123"))
    expect(res.status).toBe(502)
  })
})
