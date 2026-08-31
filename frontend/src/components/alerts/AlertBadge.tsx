import type { AlertResponse } from "@/lib/types"

const BADGE_CLASSES: Record<AlertResponse["nivel"], string> = {
  caducada: "bg-red-100 text-red-800",
  alerta_critica: "bg-orange-100 text-orange-800",
  alerta: "bg-yellow-100 text-yellow-800",
  aviso: "bg-blue-100 text-blue-800",
}

interface AlertBadgeProps {
  nivel: AlertResponse["nivel"]
}

const AlertBadge = ({ nivel }: AlertBadgeProps) => (
  <span className={`inline-flex items-center rounded px-2 py-0.5 text-xs font-medium ${BADGE_CLASSES[nivel]}`}>
    {nivel.replace(/_/g, " ")}
  </span>
)

export { AlertBadge }
