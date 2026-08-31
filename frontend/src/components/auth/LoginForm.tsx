"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { loginAction } from "@/lib/actions"

type LoginFields = {
  email: string
  password: string
}

export const LoginForm = () => {
  const [serverError, setServerError] = useState<string | null>(null)
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFields>()

  const onSubmit = async (data: LoginFields) => {
    setServerError(null)
    const formData = new FormData()
    formData.set("email", data.email)
    formData.set("password", data.password)
    const result = await loginAction(formData)
    if (result?.error) setServerError(result.error)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate className="flex flex-col gap-4 w-full max-w-sm">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
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
        <label htmlFor="password" className="block text-sm font-medium">
          Contraseña
        </label>
        <input
          id="password"
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
        {isSubmitting ? "Entrando…" : "Entrar"}
      </button>
    </form>
  )
}
