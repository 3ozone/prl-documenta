"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { signupAction } from "@/lib/actions"

type SignupFields = {
  email: string
  password: string
  confirmPassword: string
}

export const SignupForm = () => {
  const [serverError, setServerError] = useState<string | null>(null)
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<SignupFields>()

  const onSubmit = async (data: SignupFields) => {
    setServerError(null)
    const formData = new FormData()
    formData.set("email", data.email)
    formData.set("password", data.password)
    const result = await signupAction(formData)
    if (result?.error) setServerError(result.error)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate className="flex flex-col gap-4 w-full max-w-sm">
      <div>
        <label htmlFor="signup-email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="signup-email"
          type="email"
          {...register("email", {
            required: "El email es obligatorio.",
            pattern: {
              value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
              message: "Introduce un email válido.",
            },
          })}
          className="mt-1 block w-full border rounded px-3 py-2"
        />
        {errors.email && (
          <p role="alert" className="text-red-600 text-sm mt-1">
            {errors.email.message}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="signup-password" className="block text-sm font-medium">
          Contraseña
        </label>
        <input
          id="signup-password"
          type="password"
          {...register("password", {
            required: "La contraseña es obligatoria.",
            minLength: { value: 6, message: "Mínimo 6 caracteres." },
          })}
          className="mt-1 block w-full border rounded px-3 py-2"
        />
        {errors.password && (
          <p role="alert" className="text-red-600 text-sm mt-1">
            {errors.password.message}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="signup-confirm" className="block text-sm font-medium">
          Confirmar contraseña
        </label>
        <input
          id="signup-confirm"
          type="password"
          {...register("confirmPassword", {
            required: "Confirma tu contraseña.",
            validate: (val) => val === watch("password") || "Las contraseñas no coinciden.",
          })}
          className="mt-1 block w-full border rounded px-3 py-2"
        />
        {errors.confirmPassword && (
          <p role="alert" className="text-red-600 text-sm mt-1">
            {errors.confirmPassword.message}
          </p>
        )}
      </div>

      {serverError && (
        <p role="alert" className="text-red-600 text-sm">
          {serverError}
        </p>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        className="bg-blue-600 text-white rounded px-4 py-2 disabled:opacity-50"
      >
        {isSubmitting ? "Creando cuenta…" : "Crear cuenta"}
      </button>

      <p className="text-sm text-center text-gray-600">
        ¿Ya tienes cuenta?{" "}
        <a href="/login" className="text-blue-600 hover:underline">
          Inicia sesión
        </a>
      </p>
    </form>
  )
}
