import { cookies } from "next/headers"
import { redirect } from "next/navigation"
import { getRoleFromToken } from "@/lib/auth"
import { UploadTrabajadoresForm } from "@/components/categories/UploadTrabajadoresForm"

const TrabajadoresUploadPage = async () => {
  const cookieStore = await cookies()
  const token = cookieStore.get("token")?.value ?? ""
  if (getRoleFromToken(token) !== "admin") redirect("/categories/trabajadores")
  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl font-bold">Subir documento — Trabajadores</h1>
      <UploadTrabajadoresForm />
    </div>
  )
}
export default TrabajadoresUploadPage
