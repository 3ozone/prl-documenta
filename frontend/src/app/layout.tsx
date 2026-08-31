import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "PRL Documenta",
  description: "Sistema de gestión documental PRL",
}

const RootLayout = ({ children }: { children: React.ReactNode }) => (
  <html lang="es">
    <body className="bg-white min-h-screen">{children}</body>
  </html>
)

export default RootLayout
