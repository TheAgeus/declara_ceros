# Imports from selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

# Para trabajar con el teclado y mouse
import pyperclip
import pyautogui

# Other vanilla imports
import time
import pathlib
import os
import glob
import datetime
import shutil

# My globals
CURRENT_MONTH = datetime.datetime.now().month  
CURRENT_YEAR = datetime.datetime.now().year

def getRFCfromTopDirectory(directory, endChar):
    result = ""
    for c in directory:
        if c != endChar:
            result += c
        else:
            return result


def get_pass(fiel_path, fiel_folder) :
    my_password = None
    try:
        txt_full_path = glob.glob(fiel_path + fiel_folder + "\\*.txt")[0]
        file_reader = open(txt_full_path, "r")
        file_lines = [row for row in file_reader]                               
        my_password = ''
        if len(file_lines) > 0: 
            my_password = file_lines[0]
        else: 
            my_password = ''
    except:
        my_password = None
    return my_password
    

def getCredentials(fiel_path='', fiel_folder='', save_path=''):
    ruta_certificado = None
    ruta_clave_privada = None
    try:
        ruta_certificado = glob.glob(FIEL_PATH + fiel_folder + "\\*.cer")[0]
        ruta_clave_privada = glob.glob(FIEL_PATH + fiel_folder + "\\*.key")[0]
    except:
        print("Error encontrando archivos!!!")
        writeError(f"Error encontrando archivos!!!", fiel_folder=fiel_folder, save_path=ERRORS_PATH)

    password = get_pass(fiel_path, fiel_folder) 
    return ruta_certificado, ruta_clave_privada, password


def writeError(msg='', fiel_folder='', save_path='') :
    f = open(save_path + getRFCfromTopDirectory(fiel_folder, '_') + '.txt', "w+")
    f.write(msg)
    f.close()


def tryToFindElementById(driver=None, elementName='', timeout=0) : 
    segundos = 0
    element = None
    a = '..'
    b = '...'
    for i in range(timeout) :
        print(f'Buscando: {elementName} {a if segundos % 3 == 1 else b}')
        try :
            element = driver.find_element(By.ID, elementName)
            print("Elemento encontrado!! => ", elementName)
            break
        except (NoSuchElementException, UnexpectedAlertPresentException) as e:
            time.sleep(1)
            segundos = segundos + 1
    return element

def tryToFindElementByXPATH(diver=None, xPATH="", desc="", times=0):
    element = None
    cout = 0
    while element == None:
        if cout > times:
            return element
        try:
           element = driver.find_element(By.XPATH, xPATH)
        except:
            print(f"Tratando de encontrar ==> {desc}")
            cout = cout + 1
    return element
    

def tryToFindElementsByXpath(driver=None, elementsPath='', timeout=0) : 
    segundos = 0
    elements = None
    a = '..'
    b = '...'
    for i in range(timeout) :
        print(f'Buscando: {elementsPath} {a if segundos % 3 == 1 else b}')
        try :
            element = driver.find_elements(By.XPATH, elementsPath)
            print("Elementos encontrados!! => ", elementsPath)
            break
        except (NoSuchElementException, UnexpectedAlertPresentException) as e:
            time.sleep(1)
            segundos = segundos + 1
    return elements


def workaroundWrite(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy('')


def click_element(web_driver=None, elementId='', fiel_folder='', save_path='') :
    element = tryToFindElementById(driver=web_driver, elementName=elementId, timeout=5)
    if element == None :
        writeError(f"No se encontro el elemento {elementId}", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
        return False
    else: 
        try:
            element.click()
            return True
        except:
            writeError(f"Hubo un error al clickear {elementId}", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
            return False


def click_element_write_and_press_enter(web_driver=None, elementId='', fiel_folder='', save_path='', write='') : 
    click_result = click_element(web_driver=web_driver, elementId=elementId, fiel_folder=fiel_folder, save_path=save_path)
    if not click_result : return False
    time.sleep(1)
    workaroundWrite(write)
    pyautogui.press("enter")
    return True


def wait_alert(action="") :
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
        
        alert = driver.switch_to.alert
        
        print("Se encontró el alert!!!")

        if action == "acept" :
            alert.accept()
            print("Se aceptó el alert!!!")
            return True
        
        elif action == "cancel" :
            alert.dismiss()
            print("Se canceló el alert!!!")
            return True
        
    except TimeoutException:
        print("No se encontró el alert!!!")
        return False


def lastMonth():
    return CURRENT_MONTH - 1 if CURRENT_MONTH != 12 else 1 


def select_option(web_driver=None, elementId='', fiel_folder='', save_path='', index=0, wait=0, visibleText='') :
    element = tryToFindElementById(driver=web_driver, elementName=elementId, timeout=5)
    if element == None :
        writeError(f"No se encontro el elemento {elementId}", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
        return False
    else: 
        try:
            select = Select(element)
            select.select_by_index(index) if visibleText == '' else select.select_by_visible_text(visibleText)
            time.sleep(wait)
            return True
        except:
            writeError(f"Hubo un error al seleccionar {elementId} en el {'index' if visibleText == '' else 'texto'} => {index if visibleText == '' else visibleText}", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
            return False


def tabs_and_press(num_tabs=0, press='', wait=0) :
    for i in range(num_tabs):
        pyautogui.press("tab")
        time.sleep(wait)

    pyautogui.press(press)
    time.sleep(wait)



def login(ruta_cer='', ruta_key='', password='', web_driver=None):
    
    driver.get("https://ptscdecprov.clouda.sat.gob.mx/")

    # Clickear el boton de Submit
    result = click_element(web_driver=driver, elementId="buttonFiel", fiel_folder=fiel_folder, save_path=SAVE_PATH)
    if not result : return False

    # Clickear el input field donde se busca la ruta del certificado y escribir la ruta
    result = click_element_write_and_press_enter(web_driver=driver, elementId="txtCertificate", fiel_folder=fiel_folder, save_path=SAVE_PATH, write=ruta_cer)
    if not result : return False

    # Clickear el input field donde se busca la ruta del de la clave provada y escribir la ruta
    result = click_element_write_and_press_enter(web_driver=driver, elementId="txtPrivateKey", fiel_folder=fiel_folder, save_path=SAVE_PATH, write=ruta_key)
    if not result : return False

    # Clickear el input field donde se escribe la contraseña y escribirla
    result = click_element_write_and_press_enter(web_driver=driver, elementId="privateKeyPassword", fiel_folder=fiel_folder, save_path=SAVE_PATH, write=password)
    if not result : return False

    # Submit the credentials
    result = click_element(web_driver=driver, elementId="submit", fiel_folder=fiel_folder, save_path=SAVE_PATH)
    if not result : return False

    # Check if there is any errors
    element = tryToFindElementById(driver, "divError", 5)
    if element != None :
        writeError(element.get_attribute('innerHTML'), fiel_folder=fiel_folder, save_path=ERRORS_PATH)
        print("ERROR EN LOGEARTE!!!")
        return False
    else : 
        print("LOGIN EXITOSO!!!")
        return True


def fill_fields_first_form(web_driver=None, fiel_folder='', save_path='') :
    result = select_option(web_driver=web_driver, elementId="MainContent_wucConfigDeclaracion_wucDdlPeriodicidad_ddlCatalogo",
                           fiel_folder=fiel_folder, save_path=save_path, index=1, wait=3)
    if not result : return False

    if lastMonth() == 12 :
        previous_year = CURRENT_YEAR - 1
        result = select_option(web_driver=web_driver, elementId='MainContent_wucConfigDeclaracion_wucDdlEjercicioFiscal_ddlCatalogo',
                               fiel_folder=fiel_folder, save_path=save_path, wait=3, visibleText=str(previous_year))
        if not result : return False

    result = select_option(web_driver=web_driver, elementId="MainContent_wucConfigDeclaracion_wucDdlPeriodoFiscal_ddlCatalogo",
                           fiel_folder=fiel_folder, save_path=save_path, wait=3, index=lastMonth())

    tabs_and_press(num_tabs=5, press='enter', wait=0.5)
    return True


def check_obligaciones(web_driver=None, fiel_folder='', save_path='') :
    rows = tryToFindElementsByXpath(driver=web_driver, elementsPath='//table//tr', timeout=3)
    if rows == None : 
        writeError(msg="No se encontraron los checkboxes", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
        return False
    try :
        for row in rows :
            td_elements = row.find_elements(By.XPATH, './/td')
            if len(td_elements) >= 2:
                second_td_element = td_elements[1]
                # find the span element in the second td element
                span_elements = second_td_element.find_elements(By.XPATH, './/span')
                span_element = span_elements[0]

                print(span_element.get_attribute('innerHTML'))
                span_text = span_element.get_attribute('innerHTML')
                if span_text == 'IMPUESTO AL VALOR AGREGADO':
                    frist_td_checkbox_list = td_elements[0].find_elements(By.XPATH, './/input')
                    first_td_checkbox = frist_td_checkbox_list[0]
                    first_td_checkbox.click()
    except:
        writeError(msg="Error tratando de checar los checkboxes", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
        return False
    
    result = click_element(web_driver=web_driver,elementId='MainContent_btnSiguiente', fiel_folder=fiel_folder, save_path=save_path)
    if result == None : return False
    
   # wait_alert(action="acept")

    return True
##############################################################################################################################
#                                   AQUI EMPIEZA EN POCEDIMIENTO PRINCIPAL                                                   #                       
##############################################################################################################################


ROOT_PATH = pathlib.Path().resolve()                                    # Directorio raíz
FIEL_PATH = ROOT_PATH.__str__() + "\\FIEL\\"                            # Directorio donde estan las carpetas de las fieles
SAVE_PATH = ROOT_PATH.__str__() + "\\SAVE_MORAL_OLD\\"                            # Directorio donde se guardaran los pdfs
ERRORS_PATH = ROOT_PATH.__str__() + "\\ERRORS_OLD\\"                        # Directorio donde se guardaran los errores
CURRENT_MONTH = datetime.datetime.now().month                           # El mes actual
CURRENT_YEAR = datetime.datetime.now().year                             # El año actual

already_downloaded = [getRFCfromTopDirectory(f, '.') for f in os.listdir(SAVE_PATH)]
with_error = [getRFCfromTopDirectory(f, '.') for f in os.listdir(ERRORS_PATH)]

already_downloaded = already_downloaded + with_error
print(already_downloaded)
fiel_folders = [d for d in os.listdir(FIEL_PATH) if os.path.isdir(os.path.join(FIEL_PATH, d))]  # Nombre de la carpeta del empresario
remaining = [rfc for rfc in fiel_folders if getRFCfromTopDirectory(rfc, '_') not in already_downloaded] # Los que faltan por generar


for fiel_folder in remaining :  

    rfc = getRFCfromTopDirectory(fiel_folder, '_')
    if len(rfc) != 12:
        continue

    # Obtain credentials
    ruta_certificado, ruta_clave_privada, password = getCredentials(fiel_path=FIEL_PATH, fiel_folder=fiel_folder, save_path=SAVE_PATH) 
    
    # Error handling
    if ruta_certificado == None :
        writeError("No se encontro archivo .cer", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
        continue
    if ruta_clave_privada == None :
        writeError("No se enconto archivo .key", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
        continue
    if password == None :
        writeError("No se encontro la contraseña", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
        continue

    # If we have the credentials, open web browser and maximize window
    driver = webdriver.Chrome() 
    driver.maximize_window() 

    # Navigate to a web portal (SAT) and log in
    result = login(ruta_cer=ruta_certificado, ruta_key=ruta_clave_privada, password=password, web_driver=driver)
    if not result : continue

    # Cancelar el alert si es que llega a salir
    #alert = wait_alert(action="cancel")

    #with pyautogui.hold('ctrl'): pyautogui.press('t')
    #workaroundWrite("https://ptscdecprov.clouda.sat.gob.mx/Paginas/ConfigDeclaracion.aspx?opcmenu=js")
    #pyautogui.press('enter')

    # Abrir otra tab y poner la periodicidad
    driver.switch_to.new_window('')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    workaroundWrite("https://ptscdecprov.clouda.sat.gob.mx/Paginas/ConfigDeclaracion.aspx?opcmenu=js")
    pyautogui.press('enter')

    result = fill_fields_first_form(web_driver=driver, fiel_folder=fiel_folder, save_path=SAVE_PATH)

    # Este no importa si no está, pero sí importa si sí sale, porque no nos deja avanzar
    try:
        driver.find_element(By.ID, "MainContent_wucDeclaracionesTemporales_Btn_ReemplazarDeclaTemporal").click()
    except:
        print("No hubo alert de reemplazar")


    try:
        complementaria = None
        complementaria = driver.find_element(By.ID, "MainContent_btnComplementaria")
        if complementaria != None:
            pyautogui.screenshot(ERRORS_PATH + getRFCfromTopDirectory(fiel_folder, '_') + ".png")
            driver.quit()
            continue
    except:
        print("No hubo boton de complementaria")


    mas_obligaciones = tryToFindElementById(driver=driver,elementName="MainContent_wucObligaciones_ImgOtrasOblig", timeout=5)
    try:
        mas_obligaciones.click()
    except:
        print("No hay para desplegar màs obligaciones")

    time.sleep(5)

    element = tryToFindElementByXPATH(driver, "//*[text()='IMPUESTO AL VALOR AGREGADO']", "Label del checkbox", 200)
    if element == None:
        writeError("No se encontro el IMPUESTO AL VALOR AGREGADO", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
        continue

    checkbox = element.find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,"./*[1]").find_element(By.XPATH,"./*[1]")
    checkbox.click()
    click_element(web_driver=driver,elementId='MainContent_btnSiguiente', fiel_folder=fiel_folder, save_path=SAVE_PATH)

    wait_alert(action="acept")

    #wait until there are 3 handles
    while len(driver.window_handles) != 3:
        print("Esperando a que sean 3 handles")

    print("Ya son 3 handles")
    driver.switch_to.window(driver.window_handles[2])

    element = tryToFindElementByXPATH(driver, "//*[text()=' Impuesto al Valor Agregado']", "Boton de IMPUESTO AL VALOR AGREGADO", 2000)
    element.click()

    
    time.sleep(5)
    siguiente = tryToFindElementByXPATH(driver, "//*[text()='Siguiente']", "Boton de siguiente", 200)
    siguiente.click()
    time.sleep(5)

        # Por si no sale a la primera
    try:
        driver.find_element(By.XPATH, "//*[text()='Aceptar']").click()
    except:
        print("Todo continuo normal")

    time.sleep(5)

    inputs = driver.find_elements(By.CLASS_NAME, "label-danger")

    while len(inputs) == 0:
        inputs = driver.find_elements(By.CLASS_NAME, "label-danger")
        print("Aun no estan los inputs")

    for input in inputs:
        try:
            input_actual = input.find_element(By.XPATH,"..").find_element(By.TAG_NAME,"input")
            input_actual.send_keys("0")
        except:
            print("A uno no se le pudo mandar keys")

    siguiente = tryToFindElementByXPATH(driver, "//*[text()='Siguiente']", "Boton de siguiente", 200)
    siguiente.click()
    
    time.sleep(5)

    anterior = tryToFindElementByXPATH(driver, "//*[text()='Anterior']", "Boton de siguiente", 200)
    anterior.click()

    time.sleep(5)

    inputs = driver.find_elements(By.CLASS_NAME, "label-danger")

    for input in inputs:
        try:
            input_actual = input.find_element(By.XPATH,"..").find_element(By.TAG_NAME,"input")
            input_actual.send_keys("0")
        except:
            print("A uno no se le pudo mandar keys")

    time.sleep(5)

    for input in inputs:
        try:
            input_actual = input.find_element(By.XPATH,"..").find_element(By.TAG_NAME,"input")
            input_actual.send_keys("0")
        except:
            print("A uno no se le pudo mandar keys")

    time.sleep(5)

    siguiente = tryToFindElementByXPATH(driver, "//*[text()='Siguiente']", "Boton de siguiente", 200)
    siguiente.click()

    time.sleep(5)

    # Por si no sale a la primera
    try:
        driver.find_element(By.XPATH, "//*[text()='Aceptar']").click()
    except:
        print("Todo continuo normal")

    time.sleep(5)

    siguiente = tryToFindElementByXPATH(driver, "//*[text()='Siguiente']", "Boton de siguiente", 200)
    siguiente.click()

    time.sleep(5)

    # Por si no sale a la primera
    try:
        driver.find_element(By.XPATH, "//*[text()='Aceptar']").click()
    except:
        print("Todo continuo normal")


    time.sleep(2)

    element = tryToFindElementByXPATH(driver, "//*[text()='Administración de la Declaración']", "Boton de enviar delcaracion", 200)
    element.find_element(By.XPATH,"..").click()

    time.sleep(2)

    boton_enviar_declaración = tryToFindElementById(driver, "sendDecButtonID", 5)
    boton_enviar_declaración.click()
  
    time.sleep(2)
    # Por si no sale a la primera
    try:
        driver.find_element(By.XPATH, "//*[text()='Si']").click()
    except:
        print("Todo continuo normal")
    element = driver.find_element(By.XPATH, "//*[text()='Si']")

    time.sleep(5)

    # Por si sale el error
    try:
        element = driver.find_element(By.XPATH, "//*[text()='Estimado contribuyente, la declaración no puede ser enviada en este momento, favor de revisar los conceptos que desea declarar.']")
        pyautogui.screenshot(ERRORS_PATH + getRFCfromTopDirectory(fiel_folder, '_') + ".png")
        driver.quit()
        continue
    except:
        print("Todo continuo normal")

    time.sleep(5)

    driver.find_element(By.XPATH, "//*[text()='Guardar PDF']").click()
    
    # Specify the source file path and the destination directory path
    source_file = 'C:\\Users\\Ageus\\Downloads\\acusePdf.pdf'
    destination_directory = SAVE_PATH

    # Get the file name from the source file path
    file_name = os.path.basename(source_file)

    # Generate the new file name
    new_file_name = getRFCfromTopDirectory(fiel_folder, '_') + '.pdf' # Replace with your desired new file name

    # Create the new file path in the destination directory
    new_file_path = os.path.join(destination_directory, new_file_name)

    time.sleep(5)

    # Cut the file by moving it to the destination directory with the new name
    shutil.move(source_file, new_file_path)
 
    driver.quit()

