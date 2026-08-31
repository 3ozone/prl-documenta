import { cookies } from "next/headers"
import type { NextRequest } from "next/server"

export const GET = async (
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) => {
  const { id } = await params
  const cookieStore = await cookies()
  const token = cookieStore.get("token")?.value
  if (!token) return new Response(null, { status: 401 })

  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"
  const upstream = await fetch(`${apiUrl}/api/v1/documents/${id}/download`, {
    headers: { Authorization: `Bearer ${token}` },
  })

  if (!upstream.ok) {
    if (upstream.status === 404)
      return new Response("Documento no encontrado", { status: 404 })
    return new Response(null, { status: upstream.status })
  }

  return new Response(upstream.body, {
    headers: {
      "Content-Type": "application/pdf",
      "Content-Disposition": "inline",
    },
  })
}
