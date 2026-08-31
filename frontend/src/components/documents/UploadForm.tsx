"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { useRouter } from "next/navigation"

type UploadFormValues = {
  nombre_archivo: string
  fecha_validez: string
  fecha_caducidad: string
  file: FileList
}

const UploadForm = () => {
  const router = useRouter()
  const [serverError, setServerError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<UploadFormValues>()

  const onSubmit = async (data: UploadFormValues) => {
    setServerError(null)
    const formData = new FormData()
    formData.set("nombre_archivo", data.nombre_archivo)
    formData.set("fecha_validez", data.fecha_validez)
    formData.set("fecha_caducidad", data.fecha_caducidad)
    formData.set("file", data.file[0])

    const res = await fetch("/api/documents/upload", {
      method: "POST",
      body: formData,
    })

    if (res.ok) {
      setSuccess(true)
      setTimeout(() => router.push("/documents"), 1500)
    } else {
      const body = await res.json().catch(() => ({})) as { detail?: string }
      setServerError(body.detail ?? "Error al subir el documento.")
    }
  }

  if (success) {
    return <p className="text-green-600">Documento subido correctamente. Redirigiendo…</p>
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 max-w-md">
      <div>
        <label htmlFor="nombre_archivo" className="block text-sm font-medium">
          Nombre del documento
        </label>
        <input
          id="nombre_archivo"
          type="text"
          {...register("nombre_archivo", { required: "El nombre es obligatorio." })}
          className="mt-1 block w-full border rounded px-3 py-2"
        />
        {errors.nombre_archivo && (
          <p role="alert" className="text-red-600 text-sm mt-1">{errors.nombre_archivo.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="fecha_validez" className="block text-sm font-medium">
          Fecha de validez
        </label>
        <input
          id="fecha_validez"
          type="date"
          {...register("fecha_validez", { required: "La fecha de validez es obligatoria." })}
          className="mt-1 block w-full border rounded px-3 py-2"
        />
        {errors.fecha_validez && (
          <p role="alert" className="text-red-600 text-sm mt-1">{errors.fecha_validez.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="fecha_caducidad" className="block text-sm font-medium">
          Fecha de caducidad
        </label>
        <input
          id="fecha_caducidad"
          type="date"
          {...register("fecha_caducidad", { required: "La fecha de caducidad es obligatoria." })}
          className="mt-1 block w-full border rounded px-3 py-2"
        />
        {errors.fecha_caducidad && (
          <p role="alert" className="text-red-600 text-sm mt-1">{errors.fecha_caducidad.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="file" className="block text-sm font-medium">
          Archivo PDF
        </label>
        <input
          id="file"
          type="file"
          accept="application/pdf"
          {...register("file", {
            required: "Debes seleccionar un archivo.",
            validate: (fl) =>
              (fl[0]?.type === "application/pdf") || "Solo se permiten archivos PDF.",
          })}
          className="mt-1 block w-full"
        />
        {errors.file && (
          <p role="alert" className="text-red-600 text-sm mt-1">{errors.file.message}</p>
        )}
      </div>

      {serverError && (
        <p role="alert" className="text-red-600 text-sm">{serverError}</p>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        className="bg-blue-600 text-white rounded px-4 py-2 disabled:opacity-50"
      >
        {isSubmitting ? "Subiendo…" : "Subir documento"}
      </button>
    </form>
  )
}

export { UploadForm }
