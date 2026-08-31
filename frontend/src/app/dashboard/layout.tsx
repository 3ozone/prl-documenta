import { LogoutButton } from "@/components/auth/LogoutButton"

const DashboardLayout = ({ children }: { children: React.ReactNode }) => (
  <div className="min-h-screen bg-gray-50">
    <header className="bg-white border-b px-8 py-4 flex justify-between items-center">
      <span className="font-semibold text-lg">PRL Documenta</span>
      <LogoutButton />
    </header>
    <main className="p-8">{children}</main>
  </div>
)

export default DashboardLayout
