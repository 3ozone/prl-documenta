import { SignupForm } from "@/components/auth/SignupForm"

const SignupPage = () => (
  <main className="flex min-h-screen items-center justify-center bg-gray-50">
    <div className="bg-white p-8 rounded shadow-md w-full max-w-sm">
      <h1 className="text-2xl font-bold mb-6 text-center">PRL Documenta</h1>
      <p className="text-sm text-gray-600 text-center mb-6">Crea tu cuenta de acceso</p>
      <SignupForm />
    </div>
  </main>
)

export default SignupPage
