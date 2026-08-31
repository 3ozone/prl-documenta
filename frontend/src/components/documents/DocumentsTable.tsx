import { classifyStatus } from "@/lib/classifyStatus"
import type { DocumentResponse, DocumentStatus } from "@/lib/types"

const PER_PAGE = 20

const STATUS_LABELS: Record<DocumentStatus, string> = {
  vigente: "Vigente",
  proxima_a_caducar: "Próxima a caducar",
  caducada: "Caducada",
}

const STATUS_COLORS: Record<DocumentStatus, string> = {
  vigente: "text-green-700 bg-green-100",
  proxima_a_caducar: "text-yellow-700 bg-yellow-100",
  caducada: "text-red-700 bg-red-100",
}

const DocumentsTable = ({
  docs,
  page,
}: {
  docs: DocumentResponse[]
  page: number
}) => {
  const totalPages = Math.ceil(docs.length / PER_PAGE)
  const slice = docs.slice((page - 1) * PER_PAGE, page * PER_PAGE)

  return (
    <div>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="border-b bg-gray-50">
              <th className="px-4 py-2 text-left">Nombre</th>
              <th className="px-4 py-2 text-left">Fecha validez</th>
              <th className="px-4 py-2 text-left">Fecha caducidad</th>
              <th className="px-4 py-2 text-left">Estado</th>
              <th className="px-4 py-2 text-left">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {slice.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-gray-500">
                  No hay documentos.
                </td>
              </tr>
            ) : (
              slice.map((doc) => {
                const status = classifyStatus(doc)
                return (
                  <tr key={doc.id} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-2">{doc.nombre_archivo}</td>
                    <td className="px-4 py-2">{doc.fecha_validez}</td>
                    <td className="px-4 py-2">{doc.fecha_caducidad}</td>
                    <td className="px-4 py-2">
                      <span className={`rounded px-2 py-0.5 text-xs font-medium ${STATUS_COLORS[status]}`}>
                        {STATUS_LABELS[status]}
                      </span>
                    </td>
                    <td className="px-4 py-2">
                      <a
                        href={`/api/proxy/documents/${doc.id}/download`}
                        target="_blank"
                        rel="noreferrer"
                        className="text-blue-600 hover:underline text-sm"
                      >
                        Descargar
                      </a>
                    </td>
                  </tr>
                )
              })
            )}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="mt-4 flex gap-2 justify-center">
          {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
            <a
              key={p}
              href={`?page=${p}`}
              className={`rounded border px-3 py-1 text-sm ${
                p === page ? "bg-blue-600 text-white" : "text-gray-600 hover:bg-gray-50"
              }`}
            >
              {p}
            </a>
          ))}
        </div>
      )}
    </div>
  )
}

export { DocumentsTable }
