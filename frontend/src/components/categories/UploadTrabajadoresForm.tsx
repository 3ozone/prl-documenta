"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { useRouter } from "next/navigation"
import type { UploadTrabajadoresFormValues, WorkerDocumentType } from "@/lib/types"

const TIPO_LABELS: Record<WorkerDocumentType, string> = {
  formacion: "Formación",
  reconocimiento_medico: "Reconocimiento médico",
  entrega_epi: "Entrega EPI",
  aptitud_medica: "Aptitud médica",
}

const UploadTrabajadoresForm = () => {
  const router = useRouter()
  const [serverError, setServerError] = useState<string | null>(null)
  const { register, handleSubmit, formState: { errors, isSubmitting } } =
    useForm<UploadTrabajadoresFormValues>()

  const onSubmit = async (data: UploadTrabajadoresFormValues) => {
    setServerError(null)
    const fd = new FormData()
    fd.append("categoria", "trabajadores")
    fd.append("nombre_archivo", data.nombre_archivo)
    fd.append("fecha_validez", data.fecha_validez)
    fd.append("fecha_caducidad", data.fecha_caducidad)
    fd.append("file", data.file[0])
    fd.append("nombre_trabajador", data.nombre_trabajador)
    fd.append("dni", data.dni)
    fd.append("puesto", data.puesto)
    fd.append("tipo_documento", data.tipo_documento)

    const res = await fetch("/api/documents/upload", { method: "POST", body: fd })
    if (res.ok) {
      router.push("/categories/trabajadores")
    } else {
      const body = await res.json().catch(() => ({})) as { detail?: string }
      setServerError(body.detail ?? "Error al subir el documento.")
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 max-w-md">
      {/* Campos comunes */}
      <div>
        <label htmlFor="nombre_archivo_t" className="block text-sm font-medium">Nombre</label>
        <input id="nombre_archivo_t" type="text" {...register("nombre_archivo", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.nombre_archivo && <p role="alert" className="text-red-600 text-sm">{errors.nombre_archivo.message}</p>}
      </div>
      <div>
        <label htmlFor="fecha_validez_t" className="block text-sm font-medium">Fecha validez</label>
        <input id="fecha_validez_t" type="date" {...register("fecha_validez", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
      </div>
      <div>
        <label htmlFor="fecha_caducidad_t" className="block text-sm font-medium">Fecha caducidad</label>
        <input id="fecha_caducidad_t" type="date" {...register("fecha_caducidad", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
      </div>
      {/* Campos específicos */}
      <div>
        <label htmlFor="nombre_trabajador" className="block text-sm font-medium">Nombre del trabajador</label>
        <input id="nombre_trabajador" type="text" {...register("nombre_trabajador", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.nombre_trabajador && <p role="alert" className="text-red-600 text-sm">{errors.nombre_trabajador.message}</p>}
      </div>
      <div>
        <label htmlFor="dni" className="block text-sm font-medium">DNI</label>
        <input id="dni" type="text" {...register("dni", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.dni && <p role="alert" className="text-red-600 text-sm">{errors.dni.message}</p>}
      </div>
      <div>
        <label htmlFor="puesto" className="block text-sm font-medium">Puesto</label>
        <input id="puesto" type="text" {...register("puesto", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.puesto && <p role="alert" className="text-red-600 text-sm">{errors.puesto.message}</p>}
      </div>
      <div>
        <label htmlFor="tipo_documento" className="block text-sm font-medium">Tipo de documento</label>
        <select id="tipo_documento" {...register("tipo_documento", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2">
          <option value="">-- Selecciona --</option>
          {(Object.entries(TIPO_LABELS) as [WorkerDocumentType, string][]).map(([val, label]) => (
            <option key={val} value={val}>{label}</option>
          ))}
        </select>
        {errors.tipo_documento && <p role="alert" className="text-red-600 text-sm">{errors.tipo_documento.message}</p>}
      </div>
      <div>
        <label htmlFor="file_t" className="block text-sm font-medium">Archivo PDF</label>
        <input
          id="file_t"
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

export { UploadTrabajadoresForm }
