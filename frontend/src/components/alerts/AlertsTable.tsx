import type { AlertResponse } from "@/lib/types"
import { AlertBadge } from "./AlertBadge"

interface AlertsTableProps {
  alerts: AlertResponse[]
}

const AlertsTable = ({ alerts }: AlertsTableProps) => (
  <table className="w-full border-collapse text-sm">
    <thead>
      <tr className="border-b bg-gray-50 text-left">
        <th className="px-4 py-2">Documento</th>
        <th className="px-4 py-2">Categoría</th>
        <th className="px-4 py-2">Días restantes</th>
        <th className="px-4 py-2">Nivel</th>
      </tr>
    </thead>
    <tbody>
      {alerts.map((alert) => (
        <tr key={alert.document_id} className="border-b hover:bg-gray-50">
          <td className="px-4 py-2">{alert.nombre_archivo}</td>
          <td className="px-4 py-2">{alert.categoria ?? "—"}</td>
          <td className="px-4 py-2">{alert.dias_restantes}</td>
          <td className="px-4 py-2"><AlertBadge nivel={alert.nivel} /></td>
        </tr>
      ))}
    </tbody>
  </table>
)

export { AlertsTable }
