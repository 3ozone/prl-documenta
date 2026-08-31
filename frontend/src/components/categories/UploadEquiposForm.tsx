"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { useRouter } from "next/navigation"
import type { UploadEquipoFormValues } from "@/lib/types"

const UploadEquiposForm = () => {
  const router = useRouter()
  const [serverError, setServerError] = useState<string | null>(null)
  const { register, handleSubmit, watch, formState: { errors, isSubmitting } } =
    useForm<UploadEquipoFormValues>()

  const subtipo = watch("subtipo")

  const onSubmit = async (data: UploadEquipoFormValues) => {
    setServerError(null)
    const fd = new FormData()
    fd.append("categoria", "equipos")
    fd.append("nombre_archivo", data.nombre_archivo)
    fd.append("fecha_validez", data.fecha_validez)
    fd.append("fecha_caducidad", data.fecha_caducidad)
    fd.append("file", data.file[0])
    fd.append("id_equipo", data.id_equipo)
    fd.append("nombre_equipo", data.nombre_equipo)
    fd.append("numero_serie", data.numero_serie)
    fd.append("ubicacion", data.ubicacion)
    fd.append("subtipo", data.subtipo)
    if (data.subtipo === "mantenimiento") {
      if (data.tipo_mantenimiento) fd.append("tipo_mantenimiento", data.tipo_mantenimiento)
      if (data.empresa_mantenedora) fd.append("empresa_mantenedora", data.empresa_mantenedora)
      if (data.fecha_proximo_mantenimiento) fd.append("fecha_proximo_mantenimiento", data.fecha_proximo_mantenimiento)
    } else {
      if (data.organismo_inspector) fd.append("organismo_inspector", data.organismo_inspector)
      if (data.resultado_inspeccion) fd.append("resultado_inspeccion", data.resultado_inspeccion)
      if (data.fecha_proxima_inspeccion) fd.append("fecha_proxima_inspeccion", data.fecha_proxima_inspeccion)
    }

    const res = await fetch("/api/documents/upload", { method: "POST", body: fd })
    if (res.ok) {
      router.push("/categories/equipos")
    } else {
      const body = await res.json().catch(() => ({})) as { detail?: string }
      setServerError(body.detail ?? "Error al subir el documento.")
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 max-w-md">
      {/* Campos comunes */}
      <div>
        <label htmlFor="nombre_archivo_e" className="block text-sm font-medium">Nombre</label>
        <input id="nombre_archivo_e" type="text" {...register("nombre_archivo", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.nombre_archivo && <p role="alert" className="text-red-600 text-sm">{errors.nombre_archivo.message}</p>}
      </div>
      <div>
        <label htmlFor="fecha_validez_e" className="block text-sm font-medium">Fecha validez</label>
        <input id="fecha_validez_e" type="date" {...register("fecha_validez", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
      </div>
      <div>
        <label htmlFor="fecha_caducidad_e" className="block text-sm font-medium">Fecha caducidad</label>
        <input id="fecha_caducidad_e" type="date" {...register("fecha_caducidad", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
      </div>
      {/* Campos equipo */}
      <div>
        <label htmlFor="id_equipo" className="block text-sm font-medium">ID Equipo</label>
        <input id="id_equipo" type="text" {...register("id_equipo", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.id_equipo && <p role="alert" className="text-red-600 text-sm">{errors.id_equipo.message}</p>}
      </div>
      <div>
        <label htmlFor="nombre_equipo" className="block text-sm font-medium">Nombre equipo</label>
        <input id="nombre_equipo" type="text" {...register("nombre_equipo", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
        {errors.nombre_equipo && <p role="alert" className="text-red-600 text-sm">{errors.nombre_equipo.message}</p>}
      </div>
      <div>
        <label htmlFor="numero_serie" className="block text-sm font-medium">Número de serie</label>
        <input id="numero_serie" type="text" {...register("numero_serie", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
      </div>
      <div>
        <label htmlFor="ubicacion" className="block text-sm font-medium">Ubicación</label>
        <input id="ubicacion" type="text" {...register("ubicacion", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2" />
      </div>
      {/* Subtipo */}
      <div>
        <label htmlFor="subtipo" className="block text-sm font-medium">Subtipo</label>
        <select id="subtipo" {...register("subtipo", { required: "Obligatorio." })} className="mt-1 w-full border rounded px-3 py-2">
          <option value="">-- Selecciona --</option>
          <option value="mantenimiento">Mantenimiento</option>
          <option value="inspeccion">Inspección</option>
        </select>
        {errors.subtipo && <p role="alert" className="text-red-600 text-sm">{errors.subtipo.message}</p>}
      </div>
      {/* Campos condicionales mantenimiento */}
      {subtipo === "mantenimiento" && (
        <>
          <div>
            <label htmlFor="tipo_mantenimiento" className="block text-sm font-medium">Tipo mantenimiento</label>
            <input id="tipo_mantenimiento" type="text" {...register("tipo_mantenimiento")} className="mt-1 w-full border rounded px-3 py-2" />
          </div>
          <div>
            <label htmlFor="empresa_mantenedora" className="block text-sm font-medium">Empresa mantenedora</label>
            <input id="empresa_mantenedora" type="text" {...register("empresa_mantenedora")} className="mt-1 w-full border rounded px-3 py-2" />
          </div>
          <div>
            <label htmlFor="fecha_proximo_mantenimiento" className="block text-sm font-medium">Próximo mantenimiento</label>
            <input id="fecha_proximo_mantenimiento" type="date" {...register("fecha_proximo_mantenimiento")} className="mt-1 w-full border rounded px-3 py-2" />
          </div>
        </>
      )}
      {/* Campos condicionales inspección */}
      {subtipo === "inspeccion" && (
        <>
          <div>
            <label htmlFor="organismo_inspector" className="block text-sm font-medium">Organismo inspector</label>
            <input id="organismo_inspector" type="text" {...register("organismo_inspector")} className="mt-1 w-full border rounded px-3 py-2" />
          </div>
          <div>
            <label htmlFor="resultado_inspeccion" className="block text-sm font-medium">Resultado inspección</label>
            <input id="resultado_inspeccion" type="text" {...register("resultado_inspeccion")} className="mt-1 w-full border rounded px-3 py-2" />
          </div>
          <div>
            <label htmlFor="fecha_proxima_inspeccion" className="block text-sm font-medium">Próxima inspección</label>
            <input id="fecha_proxima_inspeccion" type="date" {...register("fecha_proxima_inspeccion")} className="mt-1 w-full border rounded px-3 py-2" />
          </div>
        </>
      )}
      {/* Archivo */}
      <div>
        <label htmlFor="file_e" className="block text-sm font-medium">Archivo PDF</label>
        <input
          id="file_e"
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

export { UploadEquiposForm }
