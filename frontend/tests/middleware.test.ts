import { describe, it, expect, vi, beforeEach } from "vitest"

// Mock jose before importing middleware
vi.mock("jose", () => ({
  jwtVerify: vi.fn(),
}))

// Mock next/server before importing middleware
vi.mock("next/server", () => ({
  NextResponse: {
    redirect: vi.fn((url: URL) => ({
      type: "redirect",
      location: url.toString(),
      cookies: { delete: vi.fn() },
    })),
    next: vi.fn(() => ({
      type: "next",
      cookies: { delete: vi.fn() },
    })),
  },
}))

import { jwtVerify } from "jose"
import { NextResponse } from "next/server"
import { middleware } from "../middleware"

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const makeRequest = (pathname: string, token?: string): any => ({
  nextUrl: { pathname },
  cookies: {
    get: (name: string) => (name === "token" && token ? { value: token } : undefined),
  },
  url: `http://localhost:3000${pathname}`,
})

const mockJwtValid = () =>
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  vi.mocked(jwtVerify).mockResolvedValue({} as any)

const mockJwtInvalid = () =>
  vi.mocked(jwtVerify).mockRejectedValue(new Error("Token expired"))

describe("middleware", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("R14 — redirects to /login when token is absent on protected route", async () => {
    await middleware(makeRequest("/dashboard"))
    expect(NextResponse.redirect).toHaveBeenCalledOnce()
    const target = vi.mocked(NextResponse.redirect).mock.calls[0][0] as URL
    expect(target.toString()).toContain("/login")
  })

  it("R14b — redirects to /login and clears cookie when token is expired", async () => {
    mockJwtInvalid()
    const result = await middleware(makeRequest("/dashboard", "expired-token"))
    expect(NextResponse.redirect).toHaveBeenCalledOnce()
    const target = vi.mocked(NextResponse.redirect).mock.calls[0][0] as URL
    expect(target.toString()).toContain("/login")
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    expect((result as any).cookies.delete).toHaveBeenCalledWith("token")
  })

  it("R15 — redirects to /dashboard when valid token is present on /login", async () => {
    mockJwtValid()
    await middleware(makeRequest("/login", "valid-token"))
    expect(NextResponse.redirect).toHaveBeenCalledOnce()
    const target = vi.mocked(NextResponse.redirect).mock.calls[0][0] as URL
    expect(target.toString()).toContain("/dashboard")
  })

  it("R15b — clears expired token and allows /login when token invalid on /login", async () => {
    mockJwtInvalid()
    const result = await middleware(makeRequest("/login", "expired-token"))
    expect(NextResponse.next).toHaveBeenCalledOnce()
    expect(NextResponse.redirect).not.toHaveBeenCalled()
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    expect((result as any).cookies.delete).toHaveBeenCalledWith("token")
  })

  it("R16 — allows request to pass when valid token is present on protected route", async () => {
    mockJwtValid()
    await middleware(makeRequest("/dashboard", "valid-token"))
    expect(NextResponse.next).toHaveBeenCalledOnce()
    expect(NextResponse.redirect).not.toHaveBeenCalled()
  })

  it("R13 — allows /login through when token is absent (public route)", async () => {
    await middleware(makeRequest("/login"))
    expect(NextResponse.next).toHaveBeenCalledOnce()
    expect(NextResponse.redirect).not.toHaveBeenCalled()
  })

  it("R1/R2 — redirects /reports to /login when token is absent", async () => {
    await middleware(makeRequest("/reports"))
    expect(NextResponse.redirect).toHaveBeenCalledOnce()
    const target = vi.mocked(NextResponse.redirect).mock.calls[0][0] as URL
    expect(target.toString()).toContain("/login")
  })
})
