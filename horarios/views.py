import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Materia
from .models import grupo as Grupo
from .models import MateriasAlumno, GruposAlumno
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import requests
from bs4 import BeautifulSoup
from django.core.cache import cache

    
# Pagina principal de horarios, manda los grupos y materias que un usuario autenticado a guardado
def horarios(request):
    
    if request.user.is_authenticated:
        try:
            materias_encontradas = MateriasAlumno.objects.filter(alumno=request.user).values_list('materias', flat=True)
            materias_data = []

            if materias_encontradas.exists():
                for materia_id in materias_encontradas:
                    try:
                        materia = Materia.objects.get(id=materia_id)
                        materia_data = {
                            'clave': materia.clave,
                            'nombre': materia.nombre,
                            'color': materia.color.color,
                        }
                        grupos = Grupo.objects.filter(materia=materia)
                        grupos_data = list(grupos.values())

                        materias_data.append({
                            'materia': materia_data,
                            'grupos': grupos_data,
                        })
                    except Materia.DoesNotExist:
                        print(f"Materia con id {materia_id} no existe. Verifica los datos.")
                        continue
            else:
                MateriasAlumno.objects.create(alumno=request.user)
                materias_data = []
        except MateriasAlumno.DoesNotExist:
            MateriasAlumno.objects.create(alumno=request.user)
            materias_data = []
        try:
            grupos_encontrados = GruposAlumno.objects.filter(alumno=request.user).values_list('grupos', flat=True)
            print(grupos_encontrados)
            grupos_encontrados_data=[]
            if grupos_encontrados.exists():
                for grupo_id in grupos_encontrados:
                    grupo = Grupo.objects.get(id=grupo_id)
                    grupos_encontrados_data.append({
                        "materia":grupo.materia.clave,
                        "grupo_id":grupo_id
                    })
        except GruposAlumno.DoesNotExist:
            GruposAlumno.objects.create(alumno=request.user)
            grupos_data = []
        json_data_materias = json.dumps(materias_data)
        json_data_grupos = json.dumps(grupos_encontrados_data)

        return render(request, "horarios/horarios.html", {
            'materias_data': json_data_materias,
            "grupos_data": json_data_grupos
        })
    return render(request, "horarios/horarios.html")


# Formulario para la busqueda de profesores
def formulario_maestros(request):
    if request.method == 'POST':
        tipoBusqueda = request.POST.get('tipoBusqueda')
        if tipoBusqueda == 'cadena':
            materia = request.POST.get('cadena')
            return JsonResponse({'message': 'No esta disponible la busqueda por nombre, intenta por clave'})
        elif tipoBusqueda == 'numero':
            numero = request.POST.get('numero')

            try:
                materiaEncontrada = Materia.objects.get(clave=numero)

                materia_data = {
                    'clave': materiaEncontrada.clave,
                    'nombre': materiaEncontrada.nombre,  
                    'color': materiaEncontrada.color.color,
                }
                grupos = Grupo.objects.filter(materia=materiaEncontrada)
                grupos_data = list(grupos.values())

                if request.user.is_authenticated:
                    try:
                        materia_alumno = MateriasAlumno.objects.get(alumno=request.user)
                    except MateriasAlumno.DoesNotExist:
                        materia_alumno = MateriasAlumno.objects.create(alumno=request.user)
                    materia_alumno.materias.add(materiaEncontrada)
                    materia_alumno.save()
                return JsonResponse({'message': 'Materia registrada', 'materia': materia_data, 'grupos': grupos_data})

            except Materia.DoesNotExist:
                return JsonResponse({'message': 'No se encontro la materia'})
        else:
            return JsonResponse({'message': 'Busqueda incorrecta'})
    else:
        print("Metodo GET u otro incorrecto")
        return render(request, "horarios/formulario_maestros.html")
        

#Eliminar una materia de un usuario
def deleteMateriaUsuario(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            clave = request.POST.get('clave')
            try:
                materia = Materia.objects.get(clave=clave)
                materia_alumno = MateriasAlumno.objects.get(alumno=request.user)
                materia_alumno.materias.remove(materia)
                materia_alumno.save()
                return JsonResponse({'message': 'Materia eliminada'})
            except Materia.DoesNotExist:
                return JsonResponse({'message': 'No se encontro la materia'})
        else:
            return JsonResponse({'message': 'Metodo incorrecto'})
    else:
        return JsonResponse({'message': 'Usuario no autenticado'})
    


# Guardar los grupos que el usuario a puesto en el calendario
@login_required
def guardarGrupos(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        grupos_usuario = data.get('gruposUsuario', [])
        alumno = request.user  
        try:
            GrupoAlumnoAEliminar = GruposAlumno.objects.get(alumno=alumno)
            GrupoAlumnoAEliminar.delete() 
        except GruposAlumno.DoesNotExist:
            pass  
        if grupos_usuario:
            grupos_alumno = GruposAlumno.objects.create(alumno=alumno) 
            grupos_validos = []
            for grupo_data in grupos_usuario:
                grupo_id = grupo_data.get('grupo_id')
                try:
                    grupo_obj = Grupo.objects.get(id=grupo_id)
                    grupos_validos.append(grupo_obj)
                except Grupo.DoesNotExist:
                    return JsonResponse({'error': f'El grupo con id {grupo_id} no existe'}, status=400)
            grupos_alumno.grupos.set(grupos_validos)   
            return JsonResponse({'message': 'Datos guardados correctamente'}, status=200)
        return JsonResponse({'message': 'Guardado sin grupos'}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error al procesar los datos JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)

def actualizarMateria(request, id):
    lock_id = f"actualizarMateria_lock_{id}"  # Lock único por cada materia

    # Intentar adquirir el lock (Si ya existe, otra petición la está ejecutando)
    lock = cache.add(lock_id, "lock")  # NO usamos timeout

    if not lock:
        print("aca andamos apa")
        return JsonResponse({'message': f'La materia {id} ya se está actualizando. Inténtalo más tarde.'}, status=429)

    try:
        materia = Materia.objects.get(clave=id)
        print(f"Actualizando materia con ID: {materia.id}")

        url = f"https://www.ssa.ingenieria.unam.mx/cj/tmp/programacion_horarios/{id}.html"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find('table', class_='table table-horarios-custom')

            if not table:
                return JsonResponse({'message': 'No se encontró la tabla de horarios.'}, status=404)

            tbodies = table.find_all('tbody')

            for tbody in tbodies:
                filas = tbody.find_all('tr')

                for fila in filas:
                    try:
                        datos = fila.find_all('td')
                        texto_celdas = [dato.text.strip() for dato in datos]

                        if len(texto_celdas) < 9: 
                            print("Fila con datos incompletos, omitiendo:", texto_celdas)
                            continue

                        texto_celdas[2] = re.sub(r'\n.*', '', texto_celdas[2]).strip()

                        grupo_existente = Grupo.objects.filter(
                            materia=materia,
                            grupo=int(texto_celdas[1]),
                        ).first()

                        if grupo_existente:
                            grupo_existente.grupo = int(texto_celdas[1])
                            grupo_existente.nombre = texto_celdas[2]
                            grupo_existente.tipo = texto_celdas[3]
                            grupo_existente.horas = texto_celdas[4]
                            grupo_existente.dias = texto_celdas[5]
                            grupo_existente.salon = texto_celdas[6]
                            grupo_existente.cupo = int(texto_celdas[8])

                            # if grupo_existente.calificacion == 0.0:
                            #     grupo_existente.calificacion = calificacionProfesor(texto_celdas[2])

                            grupo_existente.save()
                            print(f"Cupo actualizado para el grupo {texto_celdas[1]} de {materia.nombre}.")
                        else:
                            grupo_existente = Grupo.objects.create(
                                materia=materia,
                                grupo=int(texto_celdas[1]),
                                nombre=texto_celdas[2],
                                tipo=texto_celdas[3],
                                horas=texto_celdas[4],
                                dias=texto_celdas[5],
                                salon=texto_celdas[6],
                                cupo=int(texto_celdas[8]),
                                calificacion=calificacionProfesor(texto_celdas[2])
                            )
                            print(f"Se añadió el grupo {texto_celdas[1]} de {materia.nombre}.")

                    except Exception as e:
                        print(f"Error al procesar la clase: {e}")
                        continue

            materia_data = {
                'clave': materia.clave,
                'nombre': materia.nombre,
                'color': materia.color.color,
            }
            grupos_actualizados = list(Grupo.objects.filter(materia=materia).values())

            return JsonResponse({'message': 'Materia Actualizada', 'materiaNueva': {id: {'grupos': grupos_actualizados, 'materia': materia_data}}})

        else:
            print(f"Error {response.status_code}: No se pudo acceder a la página")
            return JsonResponse({'message': 'No se pudo acceder a la página', 'status': response.status_code}, status=response.status_code)

    finally:
        cache.delete(lock_id)  # Liberar el lock después de la ejecución, sin importar qué pase


#Funcion para la configuracion del navegador en selenium
def configurar_navegador(headless=True):
    """Configura las opciones del navegador para Selenium."""
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
    opts.add_argument("--disable-search-engine-choice-screen")
    opts.add_argument("--disable-logging")
    opts.add_argument("--log-level=3")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--headless")
    return webdriver.Chrome(options=opts)

#Funcion para buscar la calificacion de un profesor
def calificacionProfesor(nombre):
    """Busca la calificación de un profesor por nombre."""
    driver = configurar_navegador(headless=True)
    driver.implicitly_wait(5)
    try:
        driver.get('https://www.misprofesores.com/')
        inputProfesor = driver.find_element(By.XPATH, "//div[@id='navbar']//input[@class='form-control']")
        inputProfesor.send_keys(nombre)
        inputProfesor.send_keys(Keys.RETURN)
        divProfesores = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='gsc-results gsc-webResult']/div[@class='gsc-expansionArea']"))
        )
        if divProfesores:
            divProfesores[0].find_element(By.XPATH, ".//a[@class='gs-title']").click()
            WebDriverWait(driver, 5).until(lambda d: len(d.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[1])
            calificacion = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'breakdown-container')]//div[@class='grade']"))
            )
            return calificacion.text
        else:
            return "0.0"
    except Exception as e:
        print(f"Error en calificacionProfesor: {e}")
        return "0.0"
    finally:
        driver.quit()
