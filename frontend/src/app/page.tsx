import { cookies } from "next/headers"
import { redirect } from "next/navigation"

const HomePage = async () => {
  const cookieStore = await cookies()
  const token = cookieStore.get("token")?.value
  redirect(token ? "/dashboard" : "/login")
}

export default HomePage
