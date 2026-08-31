import { cookies } from "next/headers"

export const POST = async (req: Request) => {
  const cookieStore = await cookies()
  const token = cookieStore.get("token")?.value
  if (!token) return Response.json({ detail: "Unauthorized" }, { status: 401 })

  const formData = await req.formData()
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

  const upstream = await fetch(`${apiUrl}/api/v1/documents`, {
    method: "POST",
    body: formData,
    headers: { Authorization: `Bearer ${token}` },
  })

  const body = await upstream.text()
  return new Response(body, {
    status: upstream.status,
    headers: { "Content-Type": "application/json" },
  })
}
