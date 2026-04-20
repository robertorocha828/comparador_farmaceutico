from django.db import models


# 📂 Agrupa una ejecución (una carga de archivos)
class ProcesoComparacion(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Proceso {self.id} - {self.fecha_creacion}"


# 📊 Archivo Excel maestro (uno por proceso)
class ArchivoExcel(models.Model):
    proceso = models.ForeignKey(ProcesoComparacion, on_delete=models.CASCADE, related_name='excels')
    archivo = models.FileField(upload_to='excels/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Excel {self.id} - Proceso {self.proceso.id}"


# 📄 PDFs (pueden ser MUCHOS por proceso)
class ArchivoPDF(models.Model):
    proceso = models.ForeignKey(ProcesoComparacion, on_delete=models.CASCADE, related_name='pdfs')
    archivo = models.FileField(upload_to='pdfs/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PDF {self.id} - Proceso {self.proceso.id}"


# 📈 Resultado de comparación por medicamento
class ResultadoComparacion(models.Model):
    ESTADOS = [
        ('match', 'Match'),
        ('revisar', 'Revisar'),
        ('no_encontrado', 'No encontrado'),
    ]

    proceso = models.ForeignKey(ProcesoComparacion, on_delete=models.CASCADE, related_name='resultados')

    # Datos del PDF
    nombre_pdf = models.CharField(max_length=255)
    precio_pdf = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Datos del Excel
    nombre_excel = models.CharField(max_length=255, null=True, blank=True)
    precio_excel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Comparación
    similitud = models.FloatField(null=True, blank=True)
    diferencia_precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    estado = models.CharField(max_length=20, choices=ESTADOS)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_pdf} - {self.estado}"