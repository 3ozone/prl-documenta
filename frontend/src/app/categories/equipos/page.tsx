import { cookies } from "next/headers"
import { getDocuments } from "@/lib/api"
import { getRoleFromToken } from "@/lib/auth"
import { DocumentsTable } from "@/components/documents/DocumentsTable"
import log from "@/lib/logger"

const EquiposPage = async () => {
  const cookieStore = await cookies()
  const token = cookieStore.get("token")?.value ?? ""
  const role = getRoleFromToken(token)
  let docs: Awaited<ReturnType<typeof getDocuments>> = []
  let error: string | null = null
  try {
    const all = await getDocuments(token)
    docs = all.filter((d) => d.categoria === "equipos")
  } catch (err) {
    log.error({ err: String(err) }, "categories.equipos.fetch_failed")
    error = "No se pudieron cargar los documentos."
  }
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Documentos — Equipos</h1>
        {role === "admin" && (
          <a href="/categories/equipos/upload" className="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700">
            Subir documento
          </a>
        )}
      </div>
      {error ? <p className="text-red-600">{error}</p> : <DocumentsTable docs={docs} page={1} />}
    </div>
  )
}
export default EquiposPage
