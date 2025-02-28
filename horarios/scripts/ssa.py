import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from horarios.models import Materia
from horarios.models import grupo as Grupo
import requests
from bs4 import BeautifulSoup

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

def calificacionProfesor(nombre):
    """Busca la calificación de un profesor por nombre."""
    driver = configurar_navegador(headless=True)
    driver.implicitly_wait(5)  # Espera implícita global
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
            return "0.0"  # Sin calificación
    except Exception as e:
        print(f"Error en calificacionProfesor: {e}")
        return "0.0"
    finally:
        driver.quit()

def inicio(id):
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
        print('No se encontró la tabla de horarios.')
    
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

                if grupo_existente.calificacion == 0.0:
                    grupo_existente.calificacion = calificacionProfesor(texto_celdas[2])

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

materias = Materia.objects.all()
for materia in materias:
    inicio(materia.clave)
