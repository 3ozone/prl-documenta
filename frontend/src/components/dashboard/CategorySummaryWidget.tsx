import { getDocuments } from "@/lib/api"
import log from "@/lib/logger"

type Category = "empresa" | "trabajadores" | "equipos"

const CATEGORIES: Category[] = ["empresa", "trabajadores", "equipos"]
const CATEGORY_LABELS: Record<Category, string> = {
  empresa: "Empresa",
  trabajadores: "Trabajadores",
  equipos: "Equipos",
}

const CategorySummaryWidget = async ({ token }: { token: string }) => {
  const counts: Record<Category, number> = { empresa: 0, trabajadores: 0, equipos: 0 }

  try {
    const docs = await getDocuments(token)
    for (const doc of docs) {
      if (doc.categoria && doc.categoria in counts) {
        counts[doc.categoria as Category]++
      }
    }
  } catch (err) {
    log.error({ err: String(err) }, "dashboard.categories.fetch_failed")
    return (
      <div className="rounded border p-4 text-red-600">
        No se pudieron cargar los documentos por categoría.
      </div>
    )
  }

  return (
    <section className="rounded border p-4">
      <h2 className="text-lg font-semibold mb-3">Documentos por categoría</h2>
      <div className="grid grid-cols-3 gap-2">
        {CATEGORIES.map((cat) => (
          <div key={cat} className="rounded bg-gray-50 p-3 text-center">
            <p className="text-2xl font-bold text-gray-800">{counts[cat]}</p>
            <p className="text-sm text-gray-600">{CATEGORY_LABELS[cat]}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

export { CategorySummaryWidget }
