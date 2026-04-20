import pandas as pd
import pdfplumber
import re
from rapidfuzz import fuzz
import math
from .models import *


PALABRAS_RUIDO = [
    # Unidades de medida y presentaciones
    "g", "gr", "mg", "ml", "mcg", "kg", "l",
    "unid", "unidad", "unidades", "und", "un",
    "tab", "tabletas", "tableta", "tabl", "caps", "capsula", "capsulas",
    "amp", "ampolla", "ampollas", "vial", "viales", "frasco", "frascos",
    "fco", "solucion", "inyectable", "oral", "jarabe", "suspension",
    "crema", "gel", "pomada", "parche", "sobre", "sobres", "sachet",

    # Empaques y cantidades
    "caja", "cajas", "cj", "paquete", "pq", "display", "blister",
    "x", "por", "de", "con", "en",

    # Marcas y Laboratorios comunes (puedes añadir más según tus facturas)
    "genfar", "caplin", "point", "nipro", "bayer", "roche", "abbott",
    "farma", "laboratorio", "laboratorios", "ecu", "mk", "hospimed",
    "laproff", "lafrancol", "sanofi", "pfizer", "glaxo",

    # Términos de facturación o relleno
    "item", "cod", "codigo", "iva", "det", "detalle", "servicio", "bien"
]


def normalizar(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    return texto.strip()


def limpiar(texto):
    palabras = normalizar(texto).split()
    return " ".join([p for p in palabras if p not in PALABRAS_RUIDO])


def similitud(a, b):
    return fuzz.token_sort_ratio(a, b)


# 🔥 PROCESAR EXCEL ROBUSTO
import pandas as pd
import io
from .models import Medicamento, DetalleArchivo


def procesar_excel(archivo_db, file_memoria):
    """
    Procesa el Excel Maestro detectando columnas automáticamente
    y guardando cada fila en DetalleArchivo.
    """
    print(f"--- Iniciando procesamiento de Excel: {archivo_db.nombre} ---")

    try:
        # 1. Asegurar que el puntero del archivo esté al inicio
        file_memoria.seek(0)
        content = file_memoria.read()

        # 2. Leer el Excel
        df = pd.read_excel(io.BytesIO(content))

        # 3. Normalizar nombres de columnas (quitar espacios y poner en mayúsculas)
        df.columns = df.columns.str.strip().str.upper()
        print(f"Columnas detectadas: {list(df.columns)}")

        # 4. Detectar automáticamente las columnas necesarias
        col_nombre = None
        col_precio = None

        for col in df.columns:
            if any(palabra in col for palabra in ["MEDIC", "PROD", "DESCRIP", "NOMBRE"]):
                col_nombre = col
            if any(palabra in col for palabra in ["PRECIO", "VALOR", "UNIT"]):
                col_precio = col

        if not col_nombre or not col_precio:
            print(f"❌ ERROR: No se identificaron las columnas en {archivo_db.name}. Detectadas: {list(df.columns)}")
            return

        print(f"Usando columna de nombre: '{col_nombre}' y precio: '{col_precio}'")

        registros_creados = 0

        # 5. Iterar sobre las filas del Excel
        for index, row in df.iterrows():
            # Saltar filas donde el nombre del medicamento esté vacío
            if pd.isna(row.get(col_nombre)):
                continue

            try:
                nombre_original = str(row[col_nombre]).strip()

                # Obtener precio (limpiando si es necesario)
                valor_precio = row[col_precio]
                if pd.isna(valor_precio):
                    precio = 0.0
                else:
                    precio = float(valor_precio)

                # Obtener cantidad (asumimos la 4ta columna o 1 por defecto)
                try:
                    cantidad = float(row.iloc[3]) if not pd.isna(row.iloc[3]) else 1.0
                except:
                    cantidad = 1.0

                # Normalizar para la base de datos (usando tu función limpiar)
                nombre_norm = limpiar(nombre_original)

                # 6. Guardar o recuperar el Medicamento
                med, _ = Medicamento.objects.get_or_create(
                    nombre_normalizado=nombre_norm,
                    defaults={"nombre": nombre_original}
                )

                # 7. Crear el detalle vinculado al archivo y al proceso
                DetalleArchivo.objects.create(
                    archivo=archivo_db,
                    medicamento=med,
                    nombre_original=nombre_original,
                    cantidad=cantidad,
                    precio=precio,
                    subtotal=cantidad * precio
                )
                registros_creados += 1

            except Exception as e:
                print(f"Error en fila {index}: {e}")
                continue

        print(f"--- Finalizado: se crearon {registros_creados} registros desde el Excel ---")

    except Exception as e:
        print(f"❌ Error crítico procesando el archivo Excel: {e}")


# 🔥 PROCESAR PDF ROBUSTO
from decimal import Decimal, InvalidOperation
import math


def procesar_pdf(archivo, file):
    print("🔥 ENTRANDO A PROCESAR PDF POR TABLAS")

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            # Extraer tablas de la página
            tablas = page.extract_tables()

            for tabla in tablas:
                for fila in tabla:
                    # Filtro: Ignorar filas vacías o encabezados
                    if not fila or not fila[0] or "Cantidad" in str(fila[0]):
                        continue

                    try:
                        # Estructura Contifico:
                        # [0] Cantidad | [2] Producto | [4] Precio Unit | [7] Subtotal

                        raw_cantidad = str(fila[0]).split('\n')[0].replace(",", "")
                        raw_nombre = str(fila[2]).replace('\n', ' ').strip()
                        raw_precio = str(fila[4]).replace("$", "").replace(",", "").strip()
                        raw_subtotal = str(fila[-1]).replace("$", "").replace(",", "").strip()

                        cantidad = Decimal(raw_cantidad)
                        precio = Decimal(raw_precio)
                        subtotal = Decimal(raw_subtotal)

                        if cantidad <= 0: continue

                        print(f"✔ PDF Detectado: {raw_nombre} | P: {precio}")

                        nombre_norm = limpiar(raw_nombre)
                        med, _ = Medicamento.objects.get_or_create(
                            nombre_normalizado=nombre_norm,
                            defaults={"nombre": raw_nombre}
                        )

                        DetalleArchivo.objects.create(
                            archivo=archivo,
                            medicamento=med,
                            nombre_original=raw_nombre,
                            cantidad=cantidad,
                            precio=precio,
                            subtotal=subtotal
                        )
                    except (InvalidOperation, ValueError, IndexError):
                        continue

# 🔥 CONCILIACIÓN
def ejecutar_conciliacion(proceso):
    maestro = DetalleArchivo.objects.filter(
        archivo__proceso=proceso,
        archivo__tipo="maestro"
    )

    facturas = DetalleArchivo.objects.filter(
        archivo__proceso=proceso,
        archivo__tipo="factura"
    )

    print(f"📊 Maestro: {maestro.count()} | Facturas: {facturas.count()}")

    total = ok = error = revisar = 0

    for f in facturas:
        mejor = None
        mejor_score = 0

        for m in maestro:
            score = similitud(
                limpiar(f.nombre_original),
                limpiar(m.nombre_original)
            )

            if score > mejor_score:
                mejor_score = score
                mejor = m

        if not mejor:
            continue

        diferencia = abs(f.precio - mejor.precio)

        if mejor_score >= 85 and diferencia == 0:
            estado = "OK"
            ok += 1
        elif mejor_score >= 70:
            estado = "REVISAR"
            revisar += 1
        else:
            estado = "ERROR"
            error += 1

        total += 1

        Conciliacion.objects.create(
            proceso=proceso,
            archivo=f.archivo,
            medicamento=f.medicamento,
            medicamento_excel=mejor.nombre_original,
            medicamento_factura=f.nombre_original,
            cantidad=f.cantidad,
            precio_maestro=mejor.precio,
            precio_factura=f.precio,
            diferencia=diferencia,
            estado=estado,
            score_match=mejor_score,
            coincidencia_nombre=(mejor_score >= 85)
        )

    ResumenProceso.objects.update_or_create(
        proceso=proceso,
        defaults={
            "total_medicamentos": total,
            "coincidencias": ok,
            "errores": error,
            "por_revisar": revisar,
            "porcentaje_error": (error / total * 100) if total else 0
        }
    )