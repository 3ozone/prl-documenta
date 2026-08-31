import { NextRequest, NextResponse } from "next/server"
import { jwtVerify } from "jose"

const PUBLIC_ROUTES = ["/login", "/signup"]

const getSecret = () =>
  new TextEncoder().encode(
    process.env.JWT_SECRET_KEY ?? "dev-secret-change-me"
  )

const isValidToken = async (token: string): Promise<boolean> => {
  try {
    await jwtVerify(token, getSecret())
    return true
  } catch {
    return false
  }
}

export const middleware = async (request: NextRequest): Promise<NextResponse> => {
  const { pathname } = request.nextUrl
  const token = request.cookies.get("token")?.value

  const isPublic = PUBLIC_ROUTES.some((route) => pathname.startsWith(route))

  if (!isPublic) {
    if (!token || !(await isValidToken(token))) {
      // No token or expired/invalid — clear cookie and redirect to login
      const loginUrl = new URL("/login", request.url)
      const response = NextResponse.redirect(loginUrl)
      if (token) response.cookies.delete("token")
      return response
    }
  }

  if (token && pathname.startsWith("/login")) {
    if (await isValidToken(token)) {
      return NextResponse.redirect(new URL("/dashboard", request.url))
    }
    // Expired/invalid token on login page — clear it and let them log in
    const response = NextResponse.next()
    response.cookies.delete("token")
    return response
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
}
