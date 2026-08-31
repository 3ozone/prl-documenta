import { cookies } from "next/headers"
import { redirect } from "next/navigation"
import { getRoleFromToken } from "@/lib/auth"
import { UploadForm } from "@/components/documents/UploadForm"

const UploadPage = async () => {
  const cookieStore = await cookies()
  const token = cookieStore.get("token")?.value ?? ""
  const role = getRoleFromToken(token)

  if (role !== "admin") redirect("/documents")

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl font-bold">Subir documento</h1>
      <UploadForm />
    </div>
  )
}

export default UploadPage
