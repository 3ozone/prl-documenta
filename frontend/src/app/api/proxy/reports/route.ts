import { type NextRequest, NextResponse } from "next/server"

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

export async function GET(req: NextRequest): Promise<NextResponse> {
  const formato = req.nextUrl.searchParams.get("formato") ?? "csv"
  const categoria = req.nextUrl.searchParams.get("categoria") ?? "todas"
  const token = req.cookies.get("token")?.value
  if (!token) return NextResponse.json({ detail: "Unauthorized" }, { status: 401 })

  const backendUrl = `${BACKEND_URL}/api/v1/reports/status?formato=${formato}&categoria=${categoria}`
  let backendRes: Response
  try {
    backendRes = await fetch(backendUrl, {
      headers: { Authorization: `Bearer ${token}` },
    })
  } catch {
    return NextResponse.json({ detail: "Backend unavailable" }, { status: 502 })
  }

  if (backendRes.status === 401 || backendRes.status === 403) {
    return NextResponse.json({ detail: "Forbidden" }, { status: backendRes.status })
  }
  if (!backendRes.ok) {
    return NextResponse.json({ detail: "Backend error" }, { status: 502 })
  }

  const blob = await backendRes.arrayBuffer()
  const contentType = backendRes.headers.get("Content-Type") ?? "application/octet-stream"
  const contentDisposition = backendRes.headers.get("Content-Disposition") ?? ""

  return new NextResponse(blob, {
    status: 200,
    headers: {
      "Content-Type": contentType,
      ...(contentDisposition ? { "Content-Disposition": contentDisposition } : {}),
    },
  })
}
