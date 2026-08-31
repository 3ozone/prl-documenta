"use client"

import { logoutAction } from "@/lib/actions"

export const LogoutButton = () => (
  <form action={logoutAction}>
    <button
      type="submit"
      className="text-sm text-gray-600 hover:text-gray-900 underline"
    >
      Cerrar sesión
    </button>
  </form>
)
