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
asignatura['1433'] = 'ANALISIS NUMERICO'
asignatura['138'] = 'DISPOSITIVOS ELECTRONICOS'
asignatura['5138'] = 'LAB. DISPOSITIVOS ELECTRONICOS'
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

try:
    for key in asignatura:
        Materia.objects.create(clave=key, nombre=asignatura[key])  # Asegúrate de que 'clave' y 'nombre' sean los nombres de los campos en tu modelo
    print("Materias subidas con éxito")
except Exception as e:
    print("Error al subir materias :(", e)
