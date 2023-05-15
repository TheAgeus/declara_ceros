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
    

def getCredentials(fiel_path='', fiel_folder=''):
    ruta_certificado = None
    ruta_clave_privada = None
    try:
        ruta_certificado = glob.glob(FIEL_PATH + fiel_folder + "\\*.cer")[0]
        ruta_clave_privada = glob.glob(FIEL_PATH + fiel_folder + "\\*.key")[0]
    except:
        print("Error encontrando archivos")
    password = get_pass(FIEL_PATH, fiel_folder) 
    return ruta_certificado, ruta_clave_privada, password

def writeError(msg='', fiel_folder='', save_path='') :
    f = open(save_path + getRFCfromTopDirectory(fiel_folder, '_') + '.txt', "w+")
    f.write("No hay Contraseña")
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

def workaroundWrite(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy('')

def login(ruta_cer='', ruta_key='', password='', web_driver=None):
    driver.get("https://ptscdecprov.clouda.sat.gob.mx/")

    element = tryToFindElementById(driver=web_driver, elementName="buttonFiel", timeout=5)
    if element == None :
        writeError("No se encontro el elemento buttonFiel", fiel_folder=fiel_folder, save_path=SAVE_PATH)
        return None
    else: 
        element.click()

    element = tryToFindElementById(driver=web_driver, elementName="txtCertificate", timeout=10)
    if element == None :
        writeError("No se encontro el elemento txtCertificate", fiel_folder=fiel_folder, save_path=SAVE_PATH)
        return None
    else: 
        element.click()

    workaroundWrite(ruta_cer)
    pyautogui.press("enter")
##############################################################################################################################
#                                   AQUI EMPIEZA EN POCEDIMIENTO PRINCIPAL                                                   #                       
##############################################################################################################################

ROOT_PATH = pathlib.Path().resolve()                                    # Directorio raíz
FIEL_PATH = ROOT_PATH.__str__() + "\\FIEL\\"                            # Directorio donde estan las carpetas de las fieles
SAVE_PATH = ROOT_PATH.__str__() + "\\SAVE\\"                            # Directorio donde se guardaran los pdfs
ERRORS_PATH = ROOT_PATH.__str__() + "\\ERRORS\\"                        # Directorio donde se guardaran los errores
CURRENT_MONTH = datetime.datetime.now().month                           # El mes actual
CURRENT_YEAR = datetime.datetime.now().year                             # El año actual

already_downloaded = [getRFCfromTopDirectory(f, '.') for f in os.listdir(SAVE_PATH)]
print(already_downloaded)
fiel_folders = [d for d in os.listdir(FIEL_PATH) if os.path.isdir(os.path.join(FIEL_PATH, d))]  # Nombre de la carpeta del empresario
remaining = [rfc for rfc in fiel_folders if getRFCfromTopDirectory(rfc, '_') not in already_downloaded] # Los que faltan por generar

for fiel_folder in remaining :  

    # Obtain credentials
    ruta_certificado, ruta_clave_privada, password = getCredentials(fiel_path=FIEL_PATH, fiel_folder=fiel_folder) 
    
    if ruta_certificado == None :
        writeError("No se encontro archivo .cer", fiel_folder=fiel_folder, save_path=SAVE_PATH)
        continue
    if ruta_clave_privada == None :
        writeError("No se enconto archivo .key", fiel_folder=fiel_folder, save_path=SAVE_PATH)
        continue
    if password == None :
        writeError("No se encontro la contraseña", fiel_folder=fiel_folder, save_path=SAVE_PATH)
        continue

    # If we have the credentials, open web browser and maximize window
    driver = webdriver.Edge() 
    driver.maximize_window() 

    # Navigate to a web portal (SAT) and log in
    result = login(ruta_cer=ruta_certificado, ruta_key=ruta_clave_privada, password=password, web_driver=driver)
    
