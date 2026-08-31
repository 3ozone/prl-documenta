import { LoginForm } from "@/components/auth/LoginForm"

const LoginPage = async ({
  searchParams,
}: {
  searchParams: Promise<{ registered?: string }>
}) => {
  const params = await searchParams
  const registered = params.registered === "1"

  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-sm">
        <h1 className="text-2xl font-bold mb-6 text-center">PRL Documenta</h1>
        {registered && (
          <p role="status" className="text-green-700 bg-green-50 rounded px-3 py-2 text-sm text-center mb-4">
            Cuenta creada correctamente. Inicia sesión.
          </p>
        )}
        <LoginForm />
        <p className="text-sm text-center text-gray-600 mt-4">
          ¿No tienes cuenta?{" "}
          <a href="/signup" className="text-blue-600 hover:underline">
            Regístrate
          </a>
        </p>
      </div>
    </main>
  )
}

export default LoginPage
