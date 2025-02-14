import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from horarios.models import Materia, grupo

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

def inicio(numero):
    driver = configurar_navegador(headless=True)
    driver.implicitly_wait(5)
    driver.get('https://www.ssa.ingenieria.unam.mx/horarios.html')
    driver.find_element(By.XPATH, "//input[@id='clave']").send_keys(numero)
    driver.find_element(By.XPATH, "//button[@id='buscar']").click()
    clases = driver.find_elements(By.XPATH, '//tbody')[1:]  # Ignorar encabezado
    lista = []
    for clase in clases:
        if not clase.text.strip():
            continue
        try:
            datos = clase.find_elements(By.XPATH, './tr/td')
            texto_celdas = [dato.text for dato in datos]
            texto_celdas[2] = re.sub(r'\n.*', '', texto_celdas[2]).strip()
            
            try:
                materia_existente = grupo.objects.get(grupo=texto_celdas[1],nombre=texto_celdas[2],horas=texto_celdas[4],dias=texto_celdas[5])
                
                print("El profesor ya existe")
            except:
                grupo.objects.create(
                    materia=Materia.objects.get(clave=int(texto_celdas[0])),
                    grupo=texto_celdas[1],
                    nombre=texto_celdas[2],
                    tipo=texto_celdas[3],
                    horas=texto_celdas[4],
                    dias=texto_celdas[5],
                    salon=texto_celdas[6],
                    cupo=int(texto_celdas[7]),
                    calificacion=calificacionProfesor(texto_celdas[2])
                )
                print("grupo agregado con exito")
        except Exception as e:
            print(f"Error al procesar la clase: {e}")
            continue

materias = Materia.objects.all()
for materia in materias:
    inicio(materia.clave)
