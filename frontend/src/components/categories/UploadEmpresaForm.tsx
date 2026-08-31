"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { useRouter } from "next/navigation"
import type { UploadEmpresaFormValues } from "@/lib/types"

const UploadEmpresaForm = () => {
  const router = useRouter()
  const [serverError, setServerError] = useState<string | null>(null)
  const { register, handleSubmit, formState: { errors, isSubmitting } } =
    useForm<UploadEmpresaFormValues>()

  const onSubmit = async (data: UploadEmpresaFormValues) => {
    setServerError(null)
    const fd = new FormData()
    fd.append("categoria", "empresa")
    fd.append("nombre_archivo", data.nombre_archivo)
    fd.append("fecha_validez", data.fecha_validez)
    fd.append("fecha_caducidad", data.fecha_caducidad)
    fd.append("file", data.file[0])
    fd.append("razon_social", data.razon_social)
    fd.append("cif", data.cif)
    fd.append("actividad_economica", data.actividad_economica)
    fd.append("centro_trabajo", data.centro_trabajo)

    const res = await fetch("/api/documents/upload", { method: "POST", body: fd })
    if (res.ok) {
      router.push("/categories/empresa")
    } else {
      const body = await res.json().catch(() => ({})) as { detail?: string }
      setServerError(body.detail ?? "Error al subir el documento.")
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 max-w-md">
      <div>
        <label htmlFor="nombre_archivo" className="block text-sm font-medium">Nombre</label>
        <input id="nombre_archivo" type="text" {...register("nombre_archivo", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.nombre_archivo && <p role="alert" className="text-red-600 text-sm">{errors.nombre_archivo.message}</p>}
      </div>
      <div>
        <label htmlFor="fecha_validez" className="block text-sm font-medium">Fecha validez</label>
        <input id="fecha_validez" type="date" {...register("fecha_validez", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.fecha_validez && <p role="alert" className="text-red-600 text-sm">{errors.fecha_validez.message}</p>}
      </div>
      <div>
        <label htmlFor="fecha_caducidad" className="block text-sm font-medium">Fecha caducidad</label>
        <input id="fecha_caducidad" type="date" {...register("fecha_caducidad", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.fecha_caducidad && <p role="alert" className="text-red-600 text-sm">{errors.fecha_caducidad.message}</p>}
      </div>
      <div>
        <label htmlFor="razon_social" className="block text-sm font-medium">Razón social</label>
        <input id="razon_social" type="text" {...register("razon_social", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.razon_social && <p role="alert" className="text-red-600 text-sm">{errors.razon_social.message}</p>}
      </div>
      <div>
        <label htmlFor="cif" className="block text-sm font-medium">CIF</label>
        <input id="cif" type="text" {...register("cif", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.cif && <p role="alert" className="text-red-600 text-sm">{errors.cif.message}</p>}
      </div>
      <div>
        <label htmlFor="actividad_economica" className="block text-sm font-medium">Actividad económica</label>
        <input id="actividad_economica" type="text" {...register("actividad_economica", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.actividad_economica && <p role="alert" className="text-red-600 text-sm">{errors.actividad_economica.message}</p>}
      </div>
      <div>
        <label htmlFor="centro_trabajo" className="block text-sm font-medium">Centro de trabajo</label>
        <input id="centro_trabajo" type="text" {...register("centro_trabajo", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.centro_trabajo && <p role="alert" className="text-red-600 text-sm">{errors.centro_trabajo.message}</p>}
      </div>
      <div>
        <label htmlFor="file_empresa" className="block text-sm font-medium">Archivo PDF</label>
        <input
          id="file_empresa"
          type="file"
          accept="application/pdf"
          {...register("file", {
            required: "Debes seleccionar un archivo.",
            validate: (fl) => fl[0]?.type === "application/pdf" || "Solo se permiten archivos PDF.",
          })}
          className="mt-1 w-full"
        />
        {errors.file && <p role="alert" className="text-red-600 text-sm">{errors.file.message}</p>}
      </div>
      {serverError && <p role="alert" className="text-red-600 text-sm">{serverError}</p>}
      <button type="submit" disabled={isSubmitting} className="bg-blue-600 text-white rounded px-4 py-2 disabled:opacity-50">
        {isSubmitting ? "Subiendo…" : "Subir documento"}
      </button>
    </form>
  )
}

export { UploadEmpresaForm }
