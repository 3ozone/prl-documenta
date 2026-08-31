import { cookies } from "next/headers"
import { redirect } from "next/navigation"
import { AlertSummaryWidget } from "@/components/dashboard/AlertSummaryWidget"
import { CategorySummaryWidget } from "@/components/dashboard/CategorySummaryWidget"
import { StatusSummaryWidget } from "@/components/dashboard/StatusSummaryWidget"

const DashboardPage = async () => {
  const cookieStore = await cookies()
  const token = cookieStore.get("token")?.value ?? ""

  if (!token) redirect("/login")

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl font-bold">Panel de control</h1>
      <AlertSummaryWidget token={token} />
      <CategorySummaryWidget token={token} />
      <StatusSummaryWidget token={token} />
    </div>
  )
}

export default DashboardPage
