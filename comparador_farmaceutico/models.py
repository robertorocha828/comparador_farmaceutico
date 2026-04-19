from django.db import models


# ─── Proceso: agrupa una ejecución completa (un lote de archivos) ────────────
class Proceso(models.Model):
    nombre = models.CharField(max_length=255)
    mes = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proceso {self.id} - {self.nombre}"


# ─── Archivo: Excel maestro o PDF de factura, vinculado a un Proceso ─────────
class Archivo(models.Model):
    TIPOS = [
        ('maestro', 'Excel Maestro'),
        ('factura', 'Factura PDF'),
    ]
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE, related_name='archivos')
    tipo = models.CharField(max_length=10, choices=TIPOS)
    archivo = models.FileField(upload_to='uploads/')
    nombre = models.CharField(max_length=255)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.nombre}"


# ─── Medicamento: catálogo de productos normalizados ─────────────────────────
class Medicamento(models.Model):
    nombre = models.CharField(max_length=255)
    nombre_normalizado = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


# ─── DetalleArchivo: cada fila extraída de un Excel o PDF ────────────────────
class DetalleArchivo(models.Model):
    archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE, related_name='detalles')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='detalles')
    nombre_original = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nombre_original} - ${self.precio}"


# ─── Conciliacion: resultado de comparar factura vs maestro ──────────────────
class Conciliacion(models.Model):
    ESTADOS = [
        ('OK', 'Precio correcto'),
        ('REVISAR', 'Revisar'),
        ('ERROR', 'Error / No coincide'),
    ]
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE, related_name='conciliaciones')
    archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE, related_name='conciliaciones', null=True, blank=True)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='conciliaciones', null=True, blank=True)
    medicamento_excel = models.CharField(max_length=255, blank=True)
    medicamento_factura = models.CharField(max_length=255, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio_maestro = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_factura = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    diferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=10, choices=ESTADOS)
    score_match = models.FloatField(default=0)
    coincidencia_nombre = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicamento_factura} → {self.estado}"


# ─── ResumenProceso: totales del proceso de conciliación ─────────────────────
class ResumenProceso(models.Model):
    proceso = models.OneToOneField(Proceso, on_delete=models.CASCADE, related_name='resumen')
    total_medicamentos = models.IntegerField(default=0)
    coincidencias = models.IntegerField(default=0)
    errores = models.IntegerField(default=0)
    por_revisar = models.IntegerField(default=0)
    porcentaje_error = models.FloatField(default=0)

    def __str__(self):
        return f"Resumen Proceso {self.proceso.id}"