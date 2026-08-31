import { AlertsClient } from "@/components/alerts/AlertsClient"

const AlertsPage = () => (
  <div className="flex flex-col gap-6">
    <h1 className="text-2xl font-bold">Alertas activas</h1>
    <AlertsClient />
  </div>
)
export default AlertsPage
