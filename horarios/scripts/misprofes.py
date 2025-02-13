import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def calificacionProfesor(nombre):
    # Configuración de las opciones del navegador
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
    opts.add_argument("--disable-search-engine-choice-screen")
    #opts.add_argument("--headless")  # Elimina esto si no deseas usar el modo headless

    # Inicialización del navegador
    driver = webdriver.Chrome(options=opts)

    # Accede a la página
    driver.get('https://www.misprofesores.com/')

    # Encontrar el campo de búsqueda e ingresar el nombre del profesor
    inputProfesor = driver.find_element("xpath", "//div[@id='navbar']//input[@class='form-control']")
    inputProfesor.send_keys(nombre)
    inputProfesor.send_keys(Keys.RETURN)

    # Esperar a que los resultados estén disponibles (usamos WebDriverWait)
    #sleep(random.uniform(1, 3))  # Pequeña espera para no hacer peticiones muy rápidas

    # Esperamos hasta que los resultados de búsqueda estén cargados
    divProfesores = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='gsc-results gsc-webResult']/div[@class='gsc-expansionArea']"))
    )

    # Hacer clic en el primer profesor si hay resultados
    if divProfesores:
        primer_div = divProfesores[0].find_element("xpath", ".//a[@class='gs-title']")
        primer_div.click()
        print("Accediendo al primer resultado de la búsqueda...")

        # Cambiar a la nueva pestaña
        WebDriverWait(driver, 5).until(lambda d: len(d.window_handles) > 1)  # Esperar a que se abra una nueva pestaña
        driver.switch_to.window(driver.window_handles[1])  # Cambiar a la nueva pestaña

        # Esperamos a que la nueva página cargue
        #sleep(random.uniform(5, 10))  # Esperamos un poco más para asegurarnos de que la nueva página esté completamente cargada

        # Ahora, buscamos la calificación del profesor
        try:
            calificacion = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'breakdown-container')]//div[@class='grade']"))
            )
            calificacion = calificacion.text
            # Finalizamos el navegador
            driver.quit()
            return str(calificacion)  # Extraemos el texto de la calificación
        except Exception as e:
            driver.quit()
            return "S/C."
    else:
        print("S/C.")

    



