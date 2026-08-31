// @vitest-environment jsdom
import { describe, it, expect, vi } from "vitest"
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import "@testing-library/jest-dom"
import { LoginForm } from "@/components/auth/LoginForm"

vi.mock("@/lib/actions", () => ({
  loginAction: vi.fn().mockResolvedValue(undefined),
}))

describe("LoginForm", () => {
  it("shows error when email is missing", async () => {
    const user = userEvent.setup()
    render(<LoginForm />)
    await user.click(screen.getByRole("button", { name: /entrar/i }))
    expect(await screen.findByText(/email es obligatorio/i)).toBeInTheDocument()
  })

  it("shows error when email is invalid", async () => {
    const user = userEvent.setup()
    render(<LoginForm />)
    await user.type(screen.getByLabelText(/email/i), "notanemail")
    await user.click(screen.getByRole("button", { name: /entrar/i }))
    expect(await screen.findByText(/email válido/i)).toBeInTheDocument()
  })

  it("shows error when password is too short", async () => {
    const user = userEvent.setup()
    render(<LoginForm />)
    await user.type(screen.getByLabelText(/email/i), "test@example.com")
    await user.type(screen.getByLabelText(/contraseña/i), "abc")
    await user.click(screen.getByRole("button", { name: /entrar/i }))
    expect(await screen.findByText(/mínimo 6/i)).toBeInTheDocument()
  })

  it("shows server error when loginAction returns error", async () => {
    const user = userEvent.setup()
    const { loginAction } = await import("@/lib/actions")
    vi.mocked(loginAction).mockResolvedValueOnce({ error: "Credenciales incorrectas." })

    render(<LoginForm />)
    await user.type(screen.getByLabelText(/email/i), "test@example.com")
    await user.type(screen.getByLabelText(/contraseña/i), "password123")
    await user.click(screen.getByRole("button", { name: /entrar/i }))
    expect(await screen.findByText(/credenciales incorrectas/i)).toBeInTheDocument()
  })
})
