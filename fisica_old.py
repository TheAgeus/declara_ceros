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

def select_option_2(driver=None, select_element=None, visibleText=''):
    select = Select(select_element)
    select.select_by_visible_text(visibleText)

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

##############################################################################################################################
#                                   AQUI EMPIEZA EN POCEDIMIENTO PRINCIPAL                                                   #                       
##############################################################################################################################


ROOT_PATH = pathlib.Path().resolve()                                    # Directorio raíz
FIEL_PATH = ROOT_PATH.__str__() + "\\FIEL\\"                            # Directorio donde estan las carpetas de las fieles
SAVE_PATH = ROOT_PATH.__str__() + "\\SAVE_FISICA_OLD\\"                            # Directorio donde se guardaran los pdfs
ERRORS_PATH = ROOT_PATH.__str__() + "\\ERRORS\\"                        # Directorio donde se guardaran los errores
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
    if len(rfc) != 13:
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
    workaroundWrite("https://ptscdecprov.clouda.sat.gob.mx/Paginas/ConfigDeclaracion.aspx")
    pyautogui.press('enter')

    result = fill_fields_first_form(web_driver=driver, fiel_folder=fiel_folder, save_path=SAVE_PATH)

    time.sleep(3)

    try:
        driver.find_element(By.ID, "MainContent_wucDeclaracionesTemporales_Btn_ReemplazarDeclaTemporal").click
    except:
        print("No hay para reemplazar")

    time.sleep(3)

    try:
        complementaria = None
        complementaria = driver.find_element(By.ID, "MainContent_btnComplementaria")
        if complementaria != None:
            pyautogui.screenshot(ERRORS_PATH + getRFCfromTopDirectory(fiel_folder, '_') + ".png")
            driver.quit()
            continue
    except:
        print("No hubo boton de complementaria")

    try:
        driver.find_element(By.ID, "MainContent_wucObligaciones_ImgOtrasOblig").click()
    except:
        print("No hubo ")

    # Este no importa si no está, pero sí importa si sí sale, porque no nos deja avanzar
    try:
        driver.find_element(By.ID, "MainContent_wucDeclaracionesTemporales_Btn_ReemplazarDeclaTemporal").click()
    except:
        print("No hubo alert de reemplazar")

    time.sleep(5)

    element_iva = tryToFindElementByXPATH(driver, "//*[text()='IMPUESTO AL VALOR AGREGADO']", "Label del checkbox", 2000)
    if element_iva == None:
        writeError("No se encontro el IMPUESTO AL VALOR AGREGADO", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
        continue

    element_isr = tryToFindElementByXPATH(driver, "//*[text()='ISR PERSONAS FÍSICAS, ACTIVIDAD EMPRESARIAL Y PROFESIONAL']", "Label del checkbox", 2000)
    if element_isr == None:
        writeError("No se encontro el ISR PERSONAS FÍSICAS, ACTIVIDAD EMPRESARIAL Y PROFESIONAL", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
        continue


    # El Checkbox del IMPUESTO AL VALOR AGREGADO
    checkbox = element_iva.find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,"./*[1]").find_element(By.XPATH,"./*[1]")
    checkbox.click()

    # El Checkbox de ISR PERSONAS FÍSICAS, ACTIVIDAD EMPRESARIAL Y PROFESIONAL
    checkbox = element_isr.find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,"./*[1]").find_element(By.XPATH,"./*[1]")
    checkbox.click()

    click_element(web_driver=driver,elementId='MainContent_btnSiguiente', fiel_folder=fiel_folder, save_path=SAVE_PATH)

    time.sleep(3)

    try:
        driver.switch_to.alert.accept()
    except:
        print("No primer alert")

    time.sleep(3)

    try:
        driver.switch_to.alert.accept()
    except:
        print("No segundo alert")

    time.sleep(10)

    tryToFindElementByXPATH(driver, "//*[text()='IMPUESTO AL VALOR AGREGADO']", "Boton iva", 200).click()
    inputs_wrapper = driver.find_element(By.XPATH, " /html/body/div/div[2]/div/div/div/div[1]/form/div[1]/div[5]/div[2]/div[3]/div/div[1]/div[2]/div/div/div[2]")
    inputs = inputs_wrapper.find_elements(By.CLASS_NAME, "col-sm-6")
   

    for input in inputs:
        if len(input.find_elements(By.XPATH, "./*")) == 2:
            ele = input.find_element(By.XPATH, "./*[1]")
            if ele.tag_name == "input":
                try:
                    ele.send_keys("0")
                    pyautogui.press("tab")
                except: 
                    print("Not interactable")
            elif ele.tag_name == "select":
                select_option_2(driver, ele, "No")

    for input in inputs:
        if len(input.find_elements(By.XPATH, "./*")) == 2:
            ele = input.find_element(By.XPATH, "./*[1]")
            if ele.tag_name == "input":
                try:
                    ele.send_keys("0")
                    pyautogui.press("tab")
                except: 
                    print("Not interactable")
            elif ele.tag_name == "select":
                select_option_2(driver, ele, "No")


    while driver.switch_to.active_element.accessible_name != "Determinación de pago":
        pyautogui.press("tab")
    pyautogui.press("enter")
    
    while driver.switch_to.active_element.accessible_name != "Menú principal":
            pyautogui.press("tab")
    pyautogui.press("enter")

    time.sleep(5)

    tryToFindElementByXPATH(driver, "//*[text()='ISR PERSONAS FÍSICAS, ACTIVIDAD EMPRESARIAL Y PROFESIONAL']", "Boton isr", 200).click()
    inputs_wrapper = driver.find_element(By.XPATH, " /html/body/div/div[2]/div/div/div/div[1]/form/div[1]/div[5]/div[1]/div[3]/div/div[1]/div[2]/div/div/div[2]")
    inputs = inputs_wrapper.find_elements(By.CLASS_NAME, "col-sm-6")
   
    for input in inputs:
        if len(input.find_elements(By.XPATH, "./*")) == 2:
            ele = input.find_element(By.XPATH, "./*[1]")
            if ele.tag_name == "input":
                try:
                    ele.send_keys("0")
                    pyautogui.press("tab")
                except: 
                    print("Not interactable")
            elif ele.tag_name == "select":
                select_option_2(driver, ele, "No")

    for input in inputs:
        if len(input.find_elements(By.XPATH, "./*")) == 2:
            ele = input.find_element(By.XPATH, "./*[1]")
            if ele.tag_name == "input":
                try:
                    ele.send_keys("0")
                    pyautogui.press("tab")
                except: 
                    print("Not interactable")
            elif ele.tag_name == "select":
                select_option_2(driver, ele, "No")

    while driver.switch_to.active_element.accessible_name != "Determinación de pago":
        pyautogui.press("tab")
    pyautogui.press("enter")
    
    while driver.switch_to.active_element.accessible_name != "Menú principal":
            pyautogui.press("tab")
    pyautogui.press("enter")

    time.sleep(4)

    element = tryToFindElementByXPATH(driver, "//*[text()='Enviar declaración']", "Boton de enviar delcaracion", 200)
    element.find_element(By.XPATH,"..").click()

    time.sleep(5)

    driver.find_element(By.XPATH, "//*[text()='¿Desea continuar?']").find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,"*[2]").find_element(By.XPATH,"*[1]").click()

    time.sleep(10)

    driver.find_element(By.XPATH, "//*[text()='Cerrar Sesión']").find_element(By.XPATH,"..").send_keys("")
    for i in range(10):
        pyautogui.press("tab")

    pyautogui.press("enter")

    time.sleep(2)

    workaroundWrite(SAVE_PATH + rfc + ".pdf")
    pyautogui.press("enter")

    time.sleep(5)
 
    driver.quit()

