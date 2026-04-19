from django.contrib import admin
from .models import Proceso, Archivo, Medicamento, DetalleArchivo, Conciliacion, ResumenProceso

admin.site.register(Proceso)
admin.site.register(Archivo)
admin.site.register(Medicamento)
admin.site.register(DetalleArchivo)
admin.site.register(Conciliacion)
admin.site.register(ResumenProceso)
