import { cookies } from "next/headers"
import { redirect } from "next/navigation"
import { getRoleFromToken } from "@/lib/auth"
import { UploadEquiposForm } from "@/components/categories/UploadEquiposForm"

const EquiposUploadPage = async () => {
  const cookieStore = await cookies()
  const token = cookieStore.get("token")?.value ?? ""
  if (getRoleFromToken(token) !== "admin") redirect("/categories/equipos")
  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl font-bold">Subir documento — Equipos</h1>
      <UploadEquiposForm />
    </div>
  )
}
export default EquiposUploadPage
