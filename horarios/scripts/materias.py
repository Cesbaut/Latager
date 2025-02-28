# Script que sube los colores y materias a la base de datos

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'latager.settings')
django.setup()
from horarios.models import Materia
from horarios.scripts.listaAsignatura import asignatura
from horarios.models import Color  

colores = [
    {"nombre": "Rosa", "color": "#FFD1DC"},
    {"nombre": "Azul", "color": "#ADD8E6"},
    {"nombre": "Verde", "color": "#b7fadf"},
    {"nombre": "Amarillo", "color": "#FFFFE0"},
    {"nombre": "Lavanda", "color": "#E6E6FA"},
    {"nombre": "Melocoton", "color": "#FFE5B4"},
    {"nombre": "Rojo", "color": "#fcb7af"},
]

for c in colores:
    if not Color.objects.filter(color=c["color"]).exists():
        Color.objects.create(nombre=c["nombre"], color=c["color"])
        print(f"Color {c['nombre']} ({c['color']}) guardado en la base de datos.")
    else:
        print(f"Color {c['nombre']} ({c['color']}) ya existe en la base de datos.")


try:
    for key in asignatura:
        materia, creada = Materia.objects.get_or_create(clave=key, defaults={"nombre": asignatura[key]})
        if creada:
            print(f"Materia '{asignatura[key]}' creada.")
        else:
            print(f"Materia '{asignatura[key]}' ya existía.")
    print("Proceso completado.")
except Exception as e:
    print("Error al subir materias:", e)
