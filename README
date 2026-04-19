# Sistema de Automatización para Comparación de Facturas e Inventario

Proyecto desarrollado durante las prácticas preprofesionales, orientado a la automatización del proceso de validación de precios unitarios entre facturas en formato PDF y un inventario maestro en formato Excel.

## Descripción

Este sistema fue desarrollado con Django con el propósito de reducir el tiempo invertido en la revisión manual de facturas farmacéuticas. El proyecto permite cargar archivos PDF de facturas y un archivo Excel maestro de inventario para comparar nombres de productos y precios unitarios, generando resultados que facilitan la detección de inconsistencias.

## Contexto del proyecto

Durante las prácticas preprofesionales se identificó la necesidad de optimizar el proceso de revisión y conciliación de productos facturados frente a un inventario de referencia. Actualmente, este tipo de validación suele requerir revisión manual, lo que puede provocar retrasos y errores humanos. Este proyecto busca aportar una solución inicial a ese problema mediante automatización.

## Objetivo general

Desarrollar una aplicación web que permita automatizar la comparación de productos y precios unitarios entre facturas PDF y un inventario Excel.

## Objetivos específicos

- Cargar un archivo Excel maestro con el inventario de productos
- Cargar una o varias facturas en formato PDF
- Extraer información relevante desde los archivos cargados
- Normalizar nombres de productos para mejorar coincidencias
- Comparar precios unitarios entre factura e inventario
- Mostrar resultados para validación, revisión o detección de diferencias

## Tecnologías utilizadas

- Python
- Django
- SQLite
- Pandas
- pdfplumber
- RapidFuzz

## Estructura del proyecto

- `django_cmvida/`: configuración principal del proyecto Django
- `comparador_farmaceutico/`: aplicación principal del sistema
- `models.py`: definición de modelos de base de datos
- `views.py`: lógica de vistas
- `services.py`: procesamiento de archivos y conciliación
- `urls.py`: rutas del proyecto y la aplicación

## Funcionalidades implementadas

- Configuración inicial del proyecto en Django
- Definición de modelos base
- Carga de archivos Excel y PDF
- Procesamiento preliminar de datos
- Lógica inicial de comparación por similitud
- Estructura inicial para visualización de resultados

## Aporte realizado durante las prácticas

Durante el desarrollo de este proyecto se trabajó en:
- Diseño de la estructura inicial del sistema
- Configuración del entorno Django
- Modelado inicial de la base de datos
- Implementación de lógica para procesamiento de Excel
- Implementación de lógica para lectura de facturas PDF
- Construcción de la lógica de conciliación de datos
- Preparación de vistas y rutas para integración con la interfaz

## Integrantes

Proyecto desarrollado por tres integrantes:

- Integrante 1: [Nombre completo]
- Integrante 2: [Nombre completo]
- Integrante 3: [Nombre completo]

## Instalación

1. Clonar el repositorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```

2. Crear entorno virtual:
```bash
python -m venv venv
```

3. Activar entorno virtual en Windows:
```bash
venv\Scripts\activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Aplicar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Ejecutar el servidor:
```bash
python manage.py runserver
```

## Estado actual

El proyecto se encuentra en fase de desarrollo. Actualmente cuenta con la base del sistema y parte de la lógica de automatización, aunque todavía requiere ajustes de integración entre modelos, vistas y servicios para completar su funcionamiento de extremo a extremo.

## Mejoras pendientes

- Unificar completamente los modelos con la lógica de servicios
- Corregir la integración entre vistas y procesamiento
- Diseñar templates funcionales para carga y resultados
- Agregar validaciones de archivos
- Mejorar la presentación de reportes
- Implementar pruebas unitarias
- Documentar el flujo técnico completo del sistema

## Observaciones

Este repositorio corresponde a un desarrollo académico-profesional realizado en el contexto de prácticas preprofesionales, con enfoque en automatización de procesos administrativos relacionados con validación de facturación e inventario.