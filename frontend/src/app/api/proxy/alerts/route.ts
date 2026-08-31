import { cookies } from "next/headers"
import { getAlerts } from "@/lib/api"

export async function GET(): Promise<Response> {
  const cookieStore = await cookies()
  const token = cookieStore.get("token")?.value ?? ""
  if (!token) return new Response(null, { status: 401 })
  try {
    const data = await getAlerts(token)
    return Response.json(data)
  } catch {
    return new Response(null, { status: 500 })
  }
}
