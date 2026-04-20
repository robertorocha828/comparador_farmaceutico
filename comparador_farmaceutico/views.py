from django.shortcuts import render, redirect
from .services import procesar_excel, procesar_pdf, ejecutar_conciliacion
from .models import Proceso, Archivo


def subir_archivos(request):
    if request.method == "POST":
        mes = request.POST.get("mes")

        excel = request.FILES.get("excel_maestro")
        facturas = request.FILES.getlist("facturas")

        proceso = Proceso.objects.create(
            nombre=f"Conciliación {mes}",
            mes=mes
        )

        # 🔹 Excel
        if excel:
            archivo_db = Archivo.objects.create(
                proceso=proceso,
                tipo="maestro",
                archivo=excel,
                nombre=excel.name
            )
            procesar_excel(archivo_db, excel)

        # 🔹 Facturas
        for f in facturas:
            archivo_db = Archivo.objects.create(
                proceso=proceso,
                tipo="factura",
                archivo=f,
                nombre=f.name
            )
            procesar_pdf(archivo_db, f)

        # 🔹 Conciliación
        ejecutar_conciliacion(proceso)

        return redirect("ver_resultados", proceso_id=proceso.id)

    return render(request, "home.html")


def ver_resultados(request, proceso_id):
    proceso = Proceso.objects.get(id=proceso_id)
    conciliaciones = proceso.conciliaciones.all()

    return render(request, "resultado.html", {
        "proceso": proceso,
        "conciliaciones": conciliaciones
    })