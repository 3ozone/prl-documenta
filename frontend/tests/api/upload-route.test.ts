import { describe, it, expect, vi } from "vitest"

vi.mock("next/headers", () => ({
  cookies: vi.fn(),
}))

import { cookies } from "next/headers"
import { POST } from "@/app/api/documents/upload/route"

describe("POST /api/documents/upload route handler", () => {
  it("R12 — includes Authorization Bearer header when token exists", async () => {
    vi.mocked(cookies).mockResolvedValue({
      get: (name: string) => name === "token" ? { value: "mytoken123" } : undefined,
    } as any)

    const fetchMock = vi.fn().mockResolvedValue({
      status: 201,
      text: async () => JSON.stringify({ id: "abc" }),
    })
    vi.stubGlobal("fetch", fetchMock)

    const formData = new FormData()
    formData.set("nombre_archivo", "test.pdf")
    const req = new Request("http://localhost/api/documents/upload", {
      method: "POST",
      body: formData,
    })

    await POST(req)

    expect(fetchMock).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        headers: expect.objectContaining({ Authorization: "Bearer mytoken123" }),
      })
    )
    vi.unstubAllGlobals()
    vi.clearAllMocks()
  })

  it("returns 401 when no token", async () => {
    vi.mocked(cookies).mockResolvedValue({
      get: () => undefined,
    } as any)

    const formData = new FormData()
    const req = new Request("http://localhost/api/documents/upload", {
      method: "POST",
      body: formData,
    })

    const res = await POST(req)
    expect(res.status).toBe(401)
    vi.clearAllMocks()
  })
})
