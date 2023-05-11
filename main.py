# Imports from selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

# Para trabajar con excel
import openpyxl

# Para trabajar con el teclado y mouse
import pyperclip
import pyautogui

# Other vanilla imports
import time
import pathlib
import os
import glob
import datetime

def workaroundWrite(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy('')


def tryToFindElementById(driver, elementName, timeout) : 
    segundos = 0
    element = None
    for i in range(timeout) :
        try :
            element = driver.find_element(By.ID, elementName)
            print("Elemento encontrado ", elementName)
        except NoSuchElementException :
            print("Error encontrando ", elementName)
            segundos = segundos + 1
            time.sleep(1)
    return element

def get_pass(fiel_path, fiel_folder) :
    txt_full_path = glob.glob(fiel_path + fiel_folder + "\\*.txt")[0]
    file_reader = open(txt_full_path, "r")
    file_lines = [row for row in file_reader]                               
    my_password = ''
    if len(file_lines) > 0: my_password = file_lines[0]
    else: my_password = ''
    return my_password

def wait_alert(action="") :
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')

        alert = driver.switch_to.alert
        if action == "acept" :
            alert.accept()
            print("alert exist and has been acepted")
        elif action == "cancel" :
            alert.dismiss()
            print("alert exist and has been dismissed")
    except TimeoutException:
        print("no alert, no action there")

##############################################################################################################################
#                                   AQUI EMPIEZA EN POCEDIMIENTO PRINCIPAL                                                   #                       
##############################################################################################################################

ROOT_PATH = pathlib.Path().resolve()                                    # Directorio raíz
FIEL_PATH = ROOT_PATH.__str__() + "\\FIEL\\"                            # Directorio donde estan las carpetas de las fieles
SAVE_PATH = ROOT_PATH.__str__() + "\\SAVE\\"                            # Directorio donde se guardaran los pdfs
ERRORS_PATH = ROOT_PATH.__str__() + "\\ERRORS\\"                        # Directorio donde se guardaran los errores
CURRENT_MONTH = datetime.datetime.now().month                           # El mes actual
CURRENT_YEAR = datetime.datetime.now().year                             # El año actual

fiel_folders = [d for d in os.listdir(FIEL_PATH) if os.path.isdir(os.path.join(FIEL_PATH, d))]  # Nombre de la carpeta del empresario
data_file = ROOT_PATH.__str__() + "\\data.xlsx" # El archivo de excel


#xlsx = openpyxl.Workbook()
#sheet = xlsx.active
#for i in range(len(fiel_folders)) :
#    sheet['A' + str(i + 1)] = fiel_folders[i]
#xlsx.save('data.xlsx')

for fiel_folder in fiel_folders :                                                   # Para cada carpeta en la carpeta "FIEL"

    # Obteniendo las tres cosas necesarias para entrar al sistema del sat por medio de e.firma

    ruta_certificado = glob.glob(FIEL_PATH + fiel_folder + "\\*.cer")[0]        # Certificado
    ruta_clave_privada = glob.glob(FIEL_PATH + fiel_folder + "\\*.key")[0]      # Clave Privada
    password = get_pass(FIEL_PATH, fiel_folder)                                 # Contraseña

    # Create a new instance of the Edge driver
    driver = webdriver.Edge()

    driver.maximize_window()

    # Navigate to a web page
    driver.get("https://ptscdecprov.clouda.sat.gob.mx/")

    # Hasta que encuentres el elemento (boton de e.firma), sigue intentando por 10 segundos
    element = tryToFindElementById(driver, "buttonFiel", 10)

    # Si se encontró, clicarlo
    if element != None: element.click()
    time.sleep(1)

    # Hasta que encuentres el elemento (input de ubicacion del certificado .cer), sigue intentando por 10 segundos
    element = tryToFindElementById(driver, "txtCertificate", 10)
    
    # Si se encontró, clicarlo, entonces estaremos ante el file dialog del certificado
    if element != None: element.click()
    time.sleep(1)

    # Escribir el certificado_path 'ruta_certificado'
    workaroundWrite(ruta_certificado)
    pyautogui.press("enter")

    # Hasta que encuentres el elemento (input de ubicacion de la llave privada .key), sigue intentando por 10 segundos
    element = tryToFindElementById(driver, "txtPrivateKey", 10)

    # Si se encontró, clicarlo, entonces estaremos ante el file dialog de la llave
    if element != None: element.click()
    time.sleep(1)

    # Escribir el certificado_path 'ruta_certificado'
    workaroundWrite(ruta_clave_privada)
    pyautogui.press("enter")

    # Hasta que encuentres el elemento (input de ubicacion de la llave privada .key), sigue intentando por 10 segundos
    element = tryToFindElementById(driver, "privateKeyPassword", 10)

    # Si se encontró, clicarlo, entonces podremos escribir la contraseña
    if element != None: element.click()
    time.sleep(1)

    # Escribir el certificado_path 'ruta_certificado'
    workaroundWrite(password)

    # Buscar el elemento con id "submit" 
    element = tryToFindElementById(driver, "submit", 10)

    # Si lo encuentra, darle click
    if element != None: element.click()
    time.sleep(3)

    # Esperar a que salga el alert si es que sale. Si sale, darle en cancelar, si no sale, nada
    wait_alert(action="cancel")

    # Buscar el elemento con id "MainContent_wucConfigDeclaracion_wucDdlPeriodicidad_ddlCatalogo" 
    element = tryToFindElementById(driver, "MainContent_wucConfigDeclaracion_wucDdlPeriodicidad_ddlCatalogo", 10)

    # Crear un elemento tipo select para poder manipularlo
    select = Select(element)

    # Elegir el elemento 2
    select.select_by_index(1)

    # Esto es para darle tiempo a la página de regresar los datos de los select 
    time.sleep(3)

    # Obtener el mes anterior
    previous_month = CURRENT_MONTH - 1 if CURRENT_MONTH != 12 else 1 

    # Si el mes anterior es 12, el mes actual es 1, entonces, tenemos que seleccionar el ejercicio anterior (año) 
    if previous_month == 12 :

        previous_year = CURRENT_YEAR - 1

        # Obtener el elemento del select del ejercicio fiscal (año)
        element = tryToFindElementById(driver, "MainContent_wucConfigDeclaracion_wucDdlEjercicioFiscal_ddlCatalogo", 10)

        # Convertirlo en un objecto de Selenium manipulable
        select = Select(element)

        # Seleccionar el año anterior
        select.select_by_visible_text(str(previous_year))

        # Esto es para darle tiempo a la página de regresar los datos de los select 
        time.sleep(3)
        

    # Buscar el elemento con el id "MainContent_wucConfigDeclaracion_wucDdlPeriodoFiscal_ddlCatalogo"
    element = tryToFindElementById(driver, "MainContent_wucConfigDeclaracion_wucDdlPeriodoFiscal_ddlCatalogo", 10)

    # Crear un elemento tipo select para poder manipularlo
    select = Select(element)

    # Seleccionar el periodo fiscal anterior
    select.select_by_index(previous_month)    
    time.sleep(3)

    for i in range(5):
        pyautogui.press("tab")
        time.sleep(1)

    # Presionar enter
    pyautogui.press("enter")
    time.sleep(1)

    element = tryToFindElementById(driver, "MainContent_wucObligaciones_ImgOtrasOblig", 10)

    # Si lo encuentra, darle click
    if element != None: element.click()
    time.sleep(3)

    # Ahora hay que buscar en la tabla "MainContent_wucObligaciones_rptGvOtrasObligaciones_gvOtrasObligaciones_0"
    # todos los tr que tengan td que tengan span que tenga de inner html "IMPUESTO AL VALOR AGREGADO"
    # "ISR PERSONAS FÍSICAS, ACTIVIDAD EMPRESARIAL Y PROFESIONAL"
    rows = driver.find_elements(By.XPATH, '//table//tr')

    # loop through the rows to find the desired td element
    for row in rows:
        # find the second td element in the row
        td_elements = row.find_elements(By.XPATH, './/td')
        if len(td_elements) >= 2:
            second_td_element = td_elements[1]
            # find the span element in the second td element
            span_elements = second_td_element.find_elements(By.XPATH, './/span')
            span_element = span_elements[0]

            print(span_element.get_attribute('innerHTML'))
            span_text = span_element.get_attribute('innerHTML')
            if span_text == 'IMPUESTO AL VALOR AGREGADO' or span_text == 'ISR PERSONAS FÍSICAS, ACTIVIDAD EMPRESARIAL Y PROFESIONAL':
                frist_td_checkbox_list = td_elements[0].find_elements(By.XPATH, './/input')
                first_td_checkbox = frist_td_checkbox_list[0]
                first_td_checkbox.click()

    element = tryToFindElementById(driver, "MainContent_btnSiguiente", 10)
    
    # Si lo encuentra, darle click
    if element != None: element.click()
    time.sleep(3)

    # Ahora nos sadrá un alert el cuál hay que aceptar
    # Esperar a que salga el alert si es que sale. Si sale, darle en cancelar, si no sale, nada
    wait_alert(action="acept")
    time.sleep(5)

    obligaciones = driver.find_elements(By.XPATH, '//*[@id="divObligacionOtras"]/a/div/div/strong')

    for ob in obligaciones:
        
        ob.click()

        form_divs = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div/div/div/div[1]/form/div[1]/div[5]/div[1]/div[3]/div/div[1]/div[2]/div/div/div[2]/div') # obtain all child divs of div container
        for div in form_divs:
            children_div = div.find_elements(By.XPATH, './*') # obtain all child of child of div container
            if len(children_div) == 2 :
                if children_div[1].tag_name == 'i': # Para los select tengo que seleccionar 'No', y para los input tengo que escribir '0'
                    if children_div[0].tag_name == 'select' :
                        select = Select(children_div[0])
                        select.select_by_visible_text('No') # Seleccionando 'No' en selects
                    else:
                        children_div[0].send_keys('0')  # Escribiendo '0' en inputs


        # Tendía que ir al siguente paso, ya sea cambiar de obligacion o guardar la ya fullfilled

    # wait for user input
    xx = input("Presione cualquier tecla para continuar")

    # Close the browser
    driver.quit()

