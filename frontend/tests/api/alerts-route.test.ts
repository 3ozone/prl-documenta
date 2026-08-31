// @vitest-environment node
import { describe, it, expect, vi, beforeEach } from "vitest"

vi.mock("next/headers", () => ({
  cookies: vi.fn(),
}))
vi.mock("@/lib/api", () => ({
  getAlerts: vi.fn(),
}))

import { cookies } from "next/headers"
import { getAlerts } from "@/lib/api"
import { GET } from "@/app/api/proxy/alerts/route"

const mockCookies = vi.mocked(cookies)
const mockGetAlerts = vi.mocked(getAlerts)

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const makeCookieStore = (token: string | undefined): any => ({
  get: (name: string) => (name === "token" && token ? { name: "token", value: token } : undefined),
})

beforeEach(() => {
  vi.clearAllMocks()
})

describe("GET /api/proxy/alerts", () => {
  it("R14 — returns 401 when no token cookie", async () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    mockCookies.mockResolvedValue(makeCookieStore(undefined) as any)
    const res = await GET()
    expect(res.status).toBe(401)
  })

  it("R3 — returns alerts JSON when token is present", async () => {
    const alerts = [{ document_id: "1", nombre_archivo: "a.pdf", categoria: null, nivel: "aviso", dias_restantes: 5 }]
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    mockCookies.mockResolvedValue(makeCookieStore("tok123") as any)
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    mockGetAlerts.mockResolvedValue(alerts as any)
    const res = await GET()
    expect(res.status).toBe(200)
    const body = await res.json()
    expect(body).toEqual(alerts)
    expect(mockGetAlerts).toHaveBeenCalledWith("tok123")
  })
})
