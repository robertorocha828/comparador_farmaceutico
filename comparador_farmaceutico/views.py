from django.shortcuts import render, redirect, get_object_or_404
from .services import procesar_excel, procesar_pdf, ejecutar_conciliacion
from .models import Proceso, Archivo, Conciliacion, ResumenProceso


def subir_archivos(request):
    if request.method == "POST":
        mes = request.POST.get("mes", "")
        excel = request.FILES.get("excel_maestro")
        facturas = request.FILES.getlist("facturas")

        proceso = Proceso.objects.create(
            nombre=f"Conciliación {mes}" if mes else "Conciliación",
            mes=mes
        )

        # 🔹 Procesar Excel maestro
        if excel:
            archivo_db = Archivo.objects.create(
                proceso=proceso,
                tipo="maestro",
                archivo=excel,
                nombre=excel.name
            )
            procesar_excel(archivo_db, excel)

        # 🔹 Procesar facturas PDF
        for f in facturas:
            archivo_db = Archivo.objects.create(
                proceso=proceso,
                tipo="factura",
                archivo=f,
                nombre=f.name
            )
            procesar_pdf(archivo_db, f)

        # 🔹 Ejecutar conciliación
        ejecutar_conciliacion(proceso)

        return redirect("ver_resultados", proceso_id=proceso.id)

    return render(request, "home.html")


def ver_resultados(request, proceso_id):
    proceso = get_object_or_404(Proceso, id=proceso_id)
    conciliaciones = proceso.conciliaciones.all()
    resumen = ResumenProceso.objects.filter(proceso=proceso).first()

    return render(request, "resultado.html", {
        "proceso": proceso,
        "conciliaciones": conciliaciones,
        "resumen": resumen,
    })