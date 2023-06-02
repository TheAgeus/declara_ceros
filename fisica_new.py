from selenium import webdriver
import glob
import datetime
import pathlib
import os

ROOT_PATH = pathlib.Path().resolve()                                    # Directorio raíz
FIEL_PATH = ROOT_PATH.__str__() + "\\FIEL\\"                            # Directorio donde estan las carpetas de las fieles
SAVE_PATH = ROOT_PATH.__str__() + "\\SAVE_FISICA_OLD\\"                            # Directorio donde se guardaran los pdfs
ERRORS_PATH = ROOT_PATH.__str__() + "\\ERRORS\\"                        # Directorio donde se guardaran los errores
CURRENT_MONTH = datetime.datetime.now().month                           # El mes actual
CURRENT_YEAR = datetime.datetime.now().year

already_downloaded = [getRFCfromTopDirectory(f, '.') for f in os.listdir(SAVE_PATH)]
with_error = [getRFCfromTopDirectory(f, '.') for f in os.listdir(ERRORS_PATH)]
already_downloaded = already_downloaded + with_error
print(already_downloaded)
fiel_folders = [d for d in os.listdir(FIEL_PATH) if os.path.isdir(os.path.join(FIEL_PATH, d))]  # Nombre de la carpeta del empresario
remaining = [rfc for rfc in fiel_folders if getRFCfromTopDirectory(rfc, '_') not in already_downloaded] # Los que faltan por generar


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


for fiel_folder in remaining :
    
    mydriver = ir_a("https://pstcdypisr.clouda.sat.gob.mx/")

    ruta_certificado, ruta_clave_privada, password = getCredentials(fiel_path=FIEL_PATH, fiel_folder=fiel_folder, save_path=SAVE_PATH) 
