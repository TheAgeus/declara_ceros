from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Para trabajar con el teclado y mouse
import pyperclip
import pyautogui

import glob
import datetime
import pathlib
import os
import time
import asyncio

def ir_a(pagina=""):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(pagina)
    return driver

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

def getRFCfromTopDirectory(directory, endChar):
    result = ""
    for c in directory:
        if c != endChar:
            result += c
        else:
            return result

def writeError(msg='', fiel_folder='', save_path='') :
    f = open(save_path + getRFCfromTopDirectory(fiel_folder, '_') + '.txt', "w+")
    f.write(msg)
    f.close()

def getCredentials(fiel_path="", fiel_folder="", save_path=""):
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

def workaroundWrite(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy('')

def login(ruta_cer='', ruta_key='', password='', web_driver=None, fiel_folder=""):

    # Clickear el boton de Submit
    result = click_element(web_driver=web_driver, elementId="buttonFiel", fiel_folder=fiel_folder, save_path=SAVE_PATH)
    if not result : return False

    # Clickear el input field donde se busca la ruta del certificado y escribir la ruta
    result = click_element_write_and_press_enter(web_driver=web_driver, elementId="txtCertificate", fiel_folder=fiel_folder, save_path=SAVE_PATH, write=ruta_cer)
    if not result : return False

    # Clickear el input field donde se busca la ruta del de la clave provada y escribir la ruta
    result = click_element_write_and_press_enter(web_driver=web_driver, elementId="txtPrivateKey", fiel_folder=fiel_folder, save_path=SAVE_PATH, write=ruta_key)
    if not result : return False

    # Clickear el input field donde se escribe la contraseña y escribirla
    result = click_element_write_and_press_enter(web_driver=web_driver, elementId="privateKeyPassword", fiel_folder=fiel_folder, save_path=SAVE_PATH, write=password)
    if not result : return False

    # Submit the credentials
    result = click_element(web_driver=web_driver, elementId="submit", fiel_folder=fiel_folder, save_path=SAVE_PATH)
    if not result : return False

    # Check if there is any errors
    element = tryToFindElementById(web_driver, "divError", 5)
    if element != None :
        writeError(element.get_attribute('innerHTML'), fiel_folder=fiel_folder, save_path=ERRORS_PATH)
        print("ERROR EN LOGEARTE!!!")
        return False
    else : 
        print("LOGIN EXITOSO!!!")
        return True

def lastMonth():
    return CURRENT_MONTH - 1 if CURRENT_MONTH != 12 else 1 

def getYear():
    if lastMonth() == 12:
        return CURRENT_YEAR - 1
    else:
        return CURRENT_YEAR

def wait_for(webdriver=None, id="", xpath="", desc="") :
    element = None
    while element == None :
        try:
            if id != "":
                element = webdriver.find_element(By.ID, id)
            else:
                element = webdriver.find_element(By.XPATH, xpath)
        except:
            print(f"Buscando >>> {desc}")
    return element

def wait_for_img(img="", desc="", timeout=0):
    pos = None
    cout = 0
    while pos == None and cout != timeout:
        print(f"Buscando >> {desc}")
        pos = pyautogui.locateOnScreen(img)
       
        time.sleep(1)
        cout = cout + 1
    return pos

def wait_for_timeout(webdriver=None, id="", path="", desc="", timeout=0):
    element = None
    cout = 0
    while element == None and cout != timeout:
        try:
            if id != "":
                element = webdriver.find_element(By.ID, id)
            else:
                element = webdriver.find_element(By.XPATH, path)
        except:
            print(f"Buscando >>> {desc}")

        time.sleep(1)
        cout = cout + 1

    return element

def isr_simplificado_de_confianza_personas_morales(mydriver=None) :
    
    # INGRESO TAB
    supuestos_inputs = mydriver.find_elements(By.CLASS_NAME, "icon-warning-sign")
    for supuesto in supuestos_inputs :
        try:
            supuesto_select = supuesto.find_element(By.XPATH, "..").find_element(By.TAG_NAME, "select")
            actual_select = Select(supuesto_select)
            actual_select.select_by_visible_text("No")
        except:
            print("")

    # DEDUCCIONES AUTORIZADAS TAB
    time.sleep(5)
    while mydriver.switch_to.active_element.accessible_name != "Deducciones autorizadas" :
        pyautogui.press("tab")
    pyautogui.press("enter")

    wrapper = mydriver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/div[40]/div/div[2]/div")                    
    elements = wrapper.find_elements(By.XPATH, '*')

    time.sleep(3)

    supuestos_inputs = mydriver.find_elements(By.CLASS_NAME, "icon-warning-sign")
    for supuesto in supuestos_inputs :
        try:
            supuesto_select = supuesto.find_element(By.XPATH, "..").find_element(By.TAG_NAME, "select")
            actual_select = Select(supuesto_select)
            actual_select.select_by_visible_text("No")
        except:
            print("")  

    for element in elements :
        try:
            element.find_element(By.CLASS_NAME, "icon-warning-sign") # Si esto pasa, entonces hay que picarle a capturar
            element.find_element(By.TAG_NAME, "a").click()

            time.sleep(3)

            supuestos_inputs = mydriver.find_elements(By.CLASS_NAME, "icon-warning-sign")
            for supuesto in supuestos_inputs :
                try:
                    supuesto.find_element(By.XPATH, "..").find_element(By.TAG_NAME, "input").send_keys("0")
                    pyautogui.press("tab")
                except:
                    print("")
            
            time.sleep(3)

            while mydriver.switch_to.active_element.accessible_name != "CERRAR" :
                pyautogui.press("tab")
            pyautogui.press("enter")

        except:
            print("")

    # DERERMINACION TAB
    time.sleep(3)
    while mydriver.switch_to.active_element.accessible_name != "Determinación" :
        pyautogui.press("tab")
    pyautogui.press("enter")

    supuestos_inputs = mydriver.find_elements(By.CLASS_NAME, "icon-warning-sign")
    for supuesto in supuestos_inputs :
        try:
            padre = supuesto.find_element(By.XPATH, "../../..")
            padre.find_element(By.TAG_NAME, "a").click()

            supuestos_inner = mydriver.find_elements(By.CLASS_NAME, "icon-warning-sign")
            for supuesto_inner in supuestos_inner :
                try:
                    supuesto_inner.find_element(By.XPATH, "..").find_element(By.TAG_NAME, "input").send_keys("0")
                    pyautogui.press("tab")
                except:
                    print("")
            time.sleep(3)

            while mydriver.switch_to.active_element.accessible_name != "CERRAR" :
                pyautogui.press("tab")
            pyautogui.press("enter")

        except:
            print("")  
    
    # PAGO TAB
    time.sleep(3)
    while mydriver.switch_to.active_element.accessible_name != "Pago" :
        pyautogui.hotkey("shift", "tab")
    pyautogui.press("enter")

    time.sleep(3)
    supuestos_inputs = mydriver.find_elements(By.TAG_NAME, "select")
    for supuesto in supuestos_inputs :
        try:
            actual_select = Select(supuesto)
            actual_select.select_by_visible_text("No")
        except:
            print("")
    
def isr_personas_morales(mydriver=None) :
    supuestos_inputs = mydriver.find_elements(By.CLASS_NAME, "icon-warning-sign")
    for supuesto in supuestos_inputs :
        try:
            supuesto_select = supuesto.find_element(By.XPATH, "..").find_element(By.TAG_NAME, "select")
            actual_select = Select(supuesto_select)
            actual_select.select_by_visible_text("No")
        except:
            print("")

    while mydriver.switch_to.active_element.accessible_name != "Determinación" :
        pyautogui.hotkey("shift", "tab")
    pyautogui.press("enter")

    wrapper = mydriver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/div[20]/div/div[2]/div")
    elements = wrapper.find_elements(By.XPATH, '*')

    time.sleep(3)

    for element in elements :
        try:
            element.find_element(By.CLASS_NAME, "icon-warning-sign") # Si esto pasa, entonces hay que picarle a capturar
            element.find_element(By.TAG_NAME, "a").click()

            time.sleep(3)

            supuestos_inputs = mydriver.find_elements(By.CLASS_NAME, "icon-warning-sign")
            for supuesto in supuestos_inputs :
                try:
                    supuesto.find_element(By.XPATH, "..").find_element(By.TAG_NAME, "input").send_keys("0")
                    pyautogui.press("tab")
                except:
                    print("")
            time.sleep(3)
            pyautogui.press("enter")
        except:
            print("")


def iva_simplificado_confianza(mydriver=None) :
    supuestos_inputs = mydriver.find_elements(By.CLASS_NAME, "icon-warning-sign")
    for supuesto in supuestos_inputs :
        try:
            padre = supuesto.find_element(By.XPATH, "../../..")
            padre.find_element(By.TAG_NAME, "a").click()

            supuestos_inner = mydriver.find_elements(By.CLASS_NAME, "icon-warning-sign")
            for supuesto_inner in supuestos_inner :
                try:
                    supuesto_inner.find_element(By.XPATH, "..").find_element(By.TAG_NAME, "input").send_keys("0")
                    pyautogui.press("tab")
                except:
                    print("")
            time.sleep(3)

            while mydriver.switch_to.active_element.accessible_name != "CERRAR" :
                pyautogui.press("tab")
            pyautogui.press("enter")

        except:
            print("")


ROOT_PATH = pathlib.Path().resolve()                                    # Directorio raíz
FIEL_PATH = ROOT_PATH.__str__() + "\\FIEL\\"                            # Directorio donde estan las carpetas de las fieles
SAVE_PATH = ROOT_PATH.__str__() + "\\SAVE_MORAL_NEW\\"                 # Directorio donde se guardaran los pdfs
SAVE_OTHER_PATH = ROOT_PATH.__str__() + "\\SAVE_FISICA_NEW\\"
ERRORS_PATH = ROOT_PATH.__str__() + "\\ERRORS_NEW\\"                    # Directorio donde se guardaran los errores
CURRENT_MONTH = datetime.datetime.now().month                           # El mes actual
CURRENT_YEAR = datetime.datetime.now().year

already_downloaded = [getRFCfromTopDirectory(f, '.') for f in os.listdir(SAVE_PATH)]
other = [getRFCfromTopDirectory(f, '.') for f in os.listdir(SAVE_OTHER_PATH)]
with_error = [getRFCfromTopDirectory(f, '.') for f in os.listdir(ERRORS_PATH)]
already_downloaded = already_downloaded + with_error + other
fiel_folders = [d for d in os.listdir(FIEL_PATH) if os.path.isdir(os.path.join(FIEL_PATH, d))]  # Nombre de la carpeta del empresario
remaining = [rfc for rfc in fiel_folders if getRFCfromTopDirectory(rfc, '_') not in already_downloaded] # Los que faltan por generar
print("remaining")
print(remaining)
def main():

    for fiel_folder in remaining :

        rfc = getRFCfromTopDirectory(fiel_folder, '_')
        if len(rfc) != 12:
            continue

        # Ir a la página base
        mydriver = ir_a("https://pstcdypisr.clouda.sat.gob.mx/") 

        # Conseguir sus credenciales
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

        # login
        result = login(ruta_cer=ruta_certificado, ruta_key=ruta_clave_privada, password=password, web_driver=mydriver, fiel_folder=fiel_folder)
        if not result : continue

        # Boton de Presentar declaración
        wait_for(webdriver=mydriver, xpath="//*[text()='Presentar declaración']", desc="Presentar declaración").click()
        time.sleep(2)

        #Wait for posible container-temporales
        container_temporales = wait_for_timeout(webdriver=mydriver, id="container-temporales", desc="container temporales", timeout=10)

        if container_temporales != None:
            temporales = container_temporales.find_elements(By.XPATH, "*")
            for e in temporales :
                e.find_element(By.TAG_NAME, "i").click()
                time.sleep(1)
                mydriver.find_element(By.XPATH, "//*[text()='SÍ']").click()
                time.sleep(1)

        # Select ejercicio y periodicidad
        # Seleccionando el ejercicio
        element = wait_for(webdriver=mydriver, id="ejercicio", desc="Select de ejercicio")
        select_element = Select(element)
        select_element.select_by_visible_text(str(getYear()))
        time.sleep(2)

        # Seleccionando la periodicidad
        element = wait_for(webdriver=mydriver, id="periodicidad", desc="Select de periodicidad")
        select_element = Select(element)
        select_element.select_by_visible_text("1-Mensual")
        time.sleep(2)

        # Seleccionando el perido
        element = wait_for(webdriver=mydriver, id="periodos", desc="Select de periodos")
        select_element = Select(element)
        select_element.select_by_index(lastMonth())
        time.sleep(2)

        # Seleccionando el tipo de declaración
        element = wait_for(webdriver=mydriver, id="tipodeclaracion", desc="Select de tipodeclaracion")
        select_element = Select(element)
        try:
            select_element.select_by_visible_text("Normal") # también hay Normal por Corrección Fiscal
        except:
            print("Ya se le sacó normal")
            writeError("Ya se le sacó normal", fiel_folder=fiel_folder, save_path=ERRORS_PATH)
            continue
        time.sleep(2)

        # Seleccionar todas las obligaciones
        obligaciones = wait_for(webdriver=mydriver, id="sectionObligaciones", desc="Select de obligaciones")
    
        for obligacion in obligaciones.find_elements(By.XPATH, "*") :
            if not obligacion.find_element(By.TAG_NAME, "input").is_selected() :
                obligacion.find_element(By.TAG_NAME, "span").click()

        wait_for(webdriver=mydriver, id="btnSiguiente", desc="Boton Siguiente").click()
        time.sleep(3)

        pyautogui.click(pyautogui.locateOnScreen("aceptar.png"))
        
        # Por si sale lo de REEMPLAZAR
        try:
            mydriver.find_element(By.XPATH, "//*[text()='REEMPLAZAR']").click()
        except:
            print("No hubo boton de Reemplazar después del primer Siguiente")

        time.sleep(5)

        # Por si sale lo de cerrar
        pos = wait_for_img("cerrar.png", "boton de cerrar", timeout=30)
        if pos == None:
            print("No se encuentra pa cerrar")
        else:
            mydriver.find_element(By.ID, "modalPrellenado").click()
        
        try:
            mydriver.find_element(By.ID, "modalPrellenado").click()
        except:
            print("")

        time.sleep(3)

        # Tengo que seleccionar cada obligación
        obligaciones = wait_for(webdriver=mydriver, id="menu-principal", desc="obligaciones")
        
        for obligacion in obligaciones.find_elements(By.XPATH, "*") :

            obligacion_name = obligacion.find_element(By.TAG_NAME, "p").text

            obligacion.find_element(By.TAG_NAME, "span").click()

            time.sleep(3)

            select = None

            if obligacion_name == "ISR simplificado de confianza. Personas morales":
                isr_simplificado_de_confianza_personas_morales(mydriver)
            elif obligacion_name ==  'ISR personas morales' :
                isr_personas_morales(mydriver)
            elif obligacion_name == "IVA simplificado de confianza":
                iva_simplificado_confianza(mydriver)
            else:

                try:
                    mydriver.find_element(By.XPATH, "//*[text()='Sin actos o actividades']").find_element(By.XPATH, "..").click()
                    select = mydriver.find_element(By.XPATH, "//*[text()='Sin actos o actividades']").find_element(By.XPATH, "..")
                except: 
                    print("")

                if select != None : # IVA retenciones
                    select_element = Select(select)
                    select_element.select_by_visible_text("Sin actos o actividades")
                
                supuestos_inputs = mydriver.find_elements(By.CLASS_NAME, "icon-warning-sign")
                for supuesto in supuestos_inputs :
                    try:
                        supuesto.find_element(By.XPATH, "..").find_element(By.TAG_NAME, "input").send_keys("0")
                    except:
                        print("")
            
                if select != None:
                    pyautogui.press("tab")
                    pyautogui.press("enter")

            if obligacion_name != "ISR simplificado de confianza. Personas morales":
                while mydriver.switch_to.active_element.accessible_name != "Pago" :
                    pyautogui.hotkey("shift", "tab")
                pyautogui.press("enter")
        
            if select != None:
                pyautogui.click(pyautogui.locateOnScreen("aceptar.png"))

            time.sleep(3)
            mydriver.find_element(By.XPATH, "//*[text()='GUARDAR']").click()
            time.sleep(3)
            mydriver.find_element(By.XPATH, "//*[text()='Administración de la declaración']").click()
            time.sleep(3)

        mydriver.find_element(By.ID, "btnEnviaDec").click()

        time.sleep(3)

        pyautogui.press("enter")
        #pyautogui.click(pyautogui.locateOnScreen("si.png"))


        wait_for(webdriver=mydriver, id="btnCert", desc="otro login")

        # Se va a necesitar hacer el login otra vez
        time.sleep(3)
        click_element_write_and_press_enter(web_driver=mydriver, elementId="btnCert", fiel_folder=fiel_folder, save_path=ERRORS_PATH, write=ruta_certificado)
        time.sleep(3)
        click_element_write_and_press_enter(web_driver=mydriver, elementId="btnPrivateKey", fiel_folder=fiel_folder, save_path=ERRORS_PATH, write=ruta_clave_privada)
        time.sleep(3)
        click_element_write_and_press_enter(web_driver=mydriver, elementId="pwdLlavePriv", fiel_folder=fiel_folder, save_path=ERRORS_PATH, write=password)
        
        time.sleep(3)
        click_element(web_driver=mydriver, elementId="btnEnviarForm", fiel_folder=fiel_folder, save_path=ERRORS_PATH)


        flag = True
        while flag :
            try: 
                mydriver.find_element(By.XPATH, "//*[text()='DESCARGAR']").send_keys("")
                flag = False
            except:
                print("")

        time.sleep(5)

        for i in range(8):
            pyautogui.press("tab")
        
        pyautogui.press("enter")

        time.sleep(3)

        workaroundWrite(SAVE_PATH + rfc + ".pdf")

        time.sleep(5)

        pyautogui.press("enter")

        time.sleep(5)

        mydriver.close()


main()