import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'latager.settings')
django.setup()

from horarios.models import Materia

asignatura = {}

asignatura['1414'] = 'ELECTRICIDAD Y MAGNETISMO'
asignatura['1473'] = 'SEÑALES Y SISTEMAS'
asignatura['840'] = 'SISTEMAS OPERATIVOS'
asignatura['1645'] = 'DISEÑO DIGITAL MODERNO'
asignatura['1644'] = 'BASES DE DATOS'
asignatura['1643'] = 'ADMINISTRACION DE PROYECTOS DE SOFTWARE'
asignatura['442'] = 'LENGUAJES FORMALES Y AUTOMATAS'
asignatura['1531'] = 'INGENIERIA DE SOFTWARE'
asignatura['1537'] = 'FINANZAS EN LA INGENIERIA EN COMPUTACION'
asignatura['1535'] = 'DISEÑO DIGITAL VLSI'
asignatura['1562'] = 'CIRCUITOS ELECTRICOS'
asignatura['6644'] = 'LAB. BASES DE DATOS'
asignatura['6562'] = 'LAB. CIRCUITOS ELECTRICOS'
asignatura['406'] = 'INTELIGENCIA ARTIFICIAL'
asignatura['434'] = 'COMPILADORES'
asignatura['1686'] = 'SISTEMAS DE COMUNICACIONES'
asignatura['6686'] = 'LAB. SISTEMAS DE COMUNICACIONES'
asignatura['1413'] = 'INTRODUCCION A LA ECONOMIA'
asignatura['6645'] = 'LAB. DISEÑO DIGITAL MODERNO'
asignatura['6473'] = 'LAB. SEÑALES Y SISTEMAS'

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
