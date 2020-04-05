#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Provee funciones utilitarias para los scripts de sistema

# UTILS
# Autor: PABLO PIZARRO @ ppizarro
# Fecha: JUNIO 2015
# Licencia: CC BY-NC 4.0

# Importación de liberías de alto nivel
LIBSTAT = [True, True]

import cookielib
import ctypes
from functools import partial
import htmlentitydefs
import os
import random
import re
import re
import sys
import time
import urllib
from uuid import getnode as get_mac
import webbrowser


try:
    import pygame
except:
    LIBSTAT[0] = False

# Configuración de las librerías de alto nivel
reload(sys)
sys.setdefaultencoding('UTF8')  # defino la codificación UTF-8
sys.dont_write_bytecode = True  # cancelo la compilación .pyc
_actualpath = str(os.getcwd()).replace("\\", "/")
sys.path.append(_actualpath + "/lib/")
sys.path.append(_actualpath + "/lib/mechanize/")
sys.path.append(_actualpath + "/lib/pyperclip")

# Importación de librerías externas
import mechanize

# Definición de constantes
CONFIG_FOLDER = "config/"
HREF_HEADERS = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1"
CONSOLE_WRAP = -25
CMD_COLORS = {"red": 0x40, "lred": 0xC0, "gray": 0x80, "lgray": 0x70, "white": 0xF0, "blue": 0x10,
              "green": 0x20, "purple": 0x50, "yellow": 0x60, "lblue": 0x90, "lgreen": 0xA0,
              "lpurple": 0xD0, "lyellow": 0xE0}
BR_ERRORxERROR_SET_FORM = 8
BR_ERRORxERROR_SET_SUBMIT = 9
BR_ERRORxNO_ACCESS_WEB = 1
BR_ERRORxNO_FORM = 3
BR_ERRORxNO_FORMID = 2
BR_ERRORxNO_OPENED = 0
BR_ERRORxNO_SELECTED_FORM = 5
BR_ERRORxNO_VALIDID = 4
BR_ERRORxNO_VALID_SUBMIT_EMPTY = 6
BR_ERRORxNO_VALID_SUBMIT_NOT_EQUAL = 7
TAG_ERRORxCANT_RETRIEVE_HTML = 16
TAG_INIT_NOT_CORRECT_ENDING = 14
TAG_INIT_NOT_FINDED = 13
TAG_LAS_NOT_FINDED = 15
ERRORS = {
    BR_ERRORxERROR_SET_FORM: "Error al establecer el formulario activo",
    BR_ERRORxERROR_SET_SUBMIT: "Error al enviar los datos",
    BR_ERRORxNO_ACCESS_WEB: "No se puede acceder a la internet",
    BR_ERRORxNO_FORM: "No existen formularios en la página actual",
    BR_ERRORxNO_FORMID: "No existe un formulario con esa identificación",
    BR_ERRORxNO_OPENED: "La página web no ha podido ser cargada",
    BR_ERRORxNO_SELECTED_FORM: "No se ha seleccionado ningún formulario",
    BR_ERRORxNO_VALIDID: "El id ingresado no es válido",
    BR_ERRORxNO_VALID_SUBMIT_EMPTY: "Los datos del formulario no pueden estar vacíos",
    BR_ERRORxNO_VALID_SUBMIT_NOT_EQUAL: "No se satisfacen todos los datos pedidos por el formulario",
    TAG_ERRORxCANT_RETRIEVE_HTML: "No se puede devolver el texto entre los tags",
    TAG_INIT_NOT_CORRECT_ENDING: "No se ha encontrado > en el tag inicial",
    TAG_INIT_NOT_FINDED: "El tag final no ha sido encontrado en el código",
    TAG_INIT_NOT_FINDED: "El tag inicial a buscar no está en el código"
}


# Funciones de usuario
def reverseDict(old_dict):
    """Reemplaza key por def de un diccionario y retorna uno nuevo"""
    new_dict = {}
    for key in old_dict.keys():
        new_dict[old_dict[key]] = key
    return new_dict


def cleanConfigDir():
    """Elima archivos cache de la carpeta config"""
    try:
        os.remove('config/.empty')
    except:
        pass


def getMacDir(lower=False):
    """Retorna la direccion mac del sistema actual"""
    mac = ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2))
    if lower:
        mac = mac.lower()
    return mac


def getConfigValue(configFile, upper=False, autoTrue=True):
    """Lee la linea de un archivo de configuracion"""
    try:
        f = open(CONFIG_FOLDER + configFile, "r")
    except:
        error("Configuracion --{0} no definida".format(configFile), True)
    line = f.readline().strip()
    # Se comprueba si el valor es booleano
    if autoTrue and (line == "1" or line == "True" or line == "TRUE"):
        return True
    elif autoTrue and (line == "0" or line == "False" or line == "FALSE"):
        return False
    # Si no es booleano
    else:
        if upper:
            return line.upper()
        return line


def loadConfigFile(configFile):
    """Retorna todo el contenido de un archivo de configuraciones"""
    f = open(CONFIG_FOLDER + configFile, "r")
    content = ""
    for line in f:
        content += line
    f.close()
    return content


def addLineConfigFile(configFile, line):
    """Añade una linea a un archivo de configuraciones"""
    content = loadConfigFile(configFile)
    f = open(CONFIG_FOLDER + configFile, "w")
    f.write(content)
    if line not in content:
        f.write("\n" + line)
    f.close()


def setConfig(configFile, configValue):
    """Crea un archivo de configuracion con el valor configValue"""
    try:
        f = open(CONFIG_FOLDER + configFile, "w")
    except:
        error("Error al escribir en el archivo {0}".format(configFile), True)
    f.write(configValue)
    f.flush()
    f.close()


def error(msg, callExit=False):
    """Muestra un mensaje de error en pantalla"""
    print color.RED + "[ERR]" + color.END + " {0}".format(msg)
    if callExit:
        exit()


def info(msg, callExit=False):
    """Muestra un mensaje de información en pantalla"""
    print msg
    if callExit:
        exit()


def unescape(text):
    """Reemplaza los caracteres html"""

    # noinspection PyShadowingNames
    def fixup(m):
        """Remueve caracteres html"""
        text = m.group(0)
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text

    return re.sub("&#?\w+;", fixup, text)


def delAcents(text):
    """Elimina los acentos"""
    if os.name == "nt":
        text = text.replace("�?", "A").replace("É", "E").replace(
            "�?", "I").replace("Ó", "O").replace("Ú", "U")
        text = text.replace("á", "a").replace("é", "e").replace(
            "í", "i").replace("ó", "o").replace("ú", "u")
        text = text.replace("Ñ", "ñ")
    return text


def upperAcents(text):
    """Convierte los acentos a mayusculas"""
    return text.replace("á", "�?").replace("é", "É").replace("í", "�?").replace("ó", "Ó").replace("ú", "Ú")


def getError(iderr):
    """Retorna el error"""
    try:
        return ERRORS[iderr]
    except:
        return "Este código de error no está definido"


def delMatrix(matrix):
    """Borra una matriz"""
    a = len(matrix)
    if a > 0:
        for k in range(a):
            matrix.pop(0)


def getTerminalSize():
    """Devuelve las dimensiones de la consola"""
    env = os.environ

    def ioctl_GWINSZ(fdn):
        try:
            import fcntl
            import termios
            import struct

            crt = struct.unpack('hh', fcntl.ioctl(fdn, termios.TIOCGWINSZ,
                                                  '1234'))
        except:
            return
        return crt

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])


def loadFromArchive(archive, lang="Cargando archivo '{0}' ...", showState=True):
    """Carga un archivo y retorna una matriz"""
    if not showState:
        print lang.format("(...)" + archive[CONSOLE_WRAP:].replace("//", "/")).replace("\"", ""),
    try:  # Se carga el archivo
        l = list()
        archive = open(archive, "r")
        for i in archive:
            l.append(i.decode('utf-8').strip())
        archive.close()
        if showState:
            print "ok"
    except:
        if showState:
            print "error"
        l = []
    return l


def openWeb(url, event):
    """Abre una direccion web"""
    webbrowser.open(url)


def getBetween(html, a, b):
    """Retorna ell contenido entre los tags a y b"""
    try:
        posa = html.index(a)  # se encuentra el primer puntero
    except:
        return DATA_ERRORxNO_APOS_IN_DATA
    posa += len(a)
    try:
        posb = html.index(b, posa)  # se encuentra el primer puntero
    except:
        return DATA_ERRORxNO_BPOS_IN_DATA
    return html[posa:posb]


def getBetweenTags(html, tagi, tagf):  # Función que retorna un valor entre dos tags
    tagi = tagi.strip()
    tagf = tagf.strip()
    try:  # Busco el primer tag
        posi = html.index(tagi)  # busco el primer tag
        if ("<" in tagi) and (">" not in tagi):  # Si el tag incluia la viñeta < y no finalizaba
            c = 1
            while True:
                try:
                    if html[posi + c] == ">":
                        posi += (c + 1)
                        break
                    c += 1
                except:
                    return TAG_INIT_NOT_CORRECT_ENDING
        else:
            posi += len(tagi)
    except:
        return TAG_INIT_NOT_FINDED  # no se encontró el primer tag
    try:
        posf = html.index(tagf, posi)  # busco el segundo tag
    except:
        return TAG_LAS_NOT_FINDED
    try:
        return html[posi:posf]  # devuelvo la cadena entre los tags
    except:
        return TAG_ERRORxCANT_RETRIEVE_HTML


def getWithTags(html, tagi, tagf):
    """Retorna el codigo incluido los tags"""
    tagi = tagi.strip()  # elimino los espacios en blanco
    tagf = tagf.strip()
    try:
        posi = html.index(tagi)  # busco el primer tag
    except:
        return TAG_INIT_NOT_FINDED  # no se encontró el primer tag
    try:
        posf = html.index(tagf, posi)  # busco el segundo tag
        if ("<" in tagf) and (">" not in tagf):  # Si el tag incluia la viñeta < y no finalizaba
            c = 1
            while True:
                try:
                    if html[posf + c] == ">":
                        posf += (c + 1)
                        break
                    c += 1
                except:
                    return TAG_INIT_NOT_CORRECT_ENDING
        else:
            posf += len(tagf)
    except:
        return TAG_LAS_NOT_FINDED
    try:
        return html[posi:posf]  # devuelvo la cadena entre los tags
    except:
        return TAG_ERRORxCANT_RETRIEVE_HTML


# Definicion de clases
class Browser:
    """Navegador web"""

    def __init__(self):  # Función constuctora
        self.br = mechanize.Browser()  # navegador
        self.cookies = cookielib.LWPCookieJar()  # cookies
        self.br.set_cookiejar(self.cookies)
        self.opened = False  # define si una páginas se ha cargado
        self.selectedForm = False  # define si se ha definido un formulario

        # Opciones del navegador
        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_refresh(False)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(
            mechanize._http.HTTPRefreshProcessor(), max_time=1)

    def playBrowser(self):  # Obtener el browser
        return self.br

    def addHeaders(self, header):  # Agregar headers al navegador
        self.br.addheaders = [('User-agent', header)]

    def abrirLink(self, web):  # Ingresar a una dirección web
        try:  # Intento cargar la web
            self.br.open(web)
            self.opened = True
            self.selectedForm = False
        except:
            return BR_ERRORxNO_ACCESS_WEB

    def getHtml(self):  # Obtener el código html
        if self.opened:
            return self.br.response().read()
        else:
            return BR_ERRORxNO_OPENED

    def getTitle(self):  # Obtener el título
        if self.opened:
            return self.br.title()
        else:
            return BR_ERRORxNO_OPENED

    def getHeaders(self):  # Obtener los headers
        if self.opened:
            return self.br.response().info()
        else:
            return BR_ERRORxNO_OPENED

    def getForms(self):  # Obtener los forms
        if self.opened:
            return self.br.forms()
        else:
            return BR_ERRORxNO_OPENED

    def selectFormById(self, formid):  # Definir un formulario como activo mediante un id
        formid = str(formid)
        if formid != "":  # Si el id no está vacío
            if formid.isdigit():  # Si es un dígito
                try:
                    self.selectedForm = True
                    return self.br.select_form(nr=int(formid))
                except:
                    return BR_ERRORxERROR_SET_FORM
            else:
                return BR_ERRORxNO_VALIDID
        else:
            return BR_ERRORxNO_FORMID

    # Definir un formulario como activo mediante un id
    def selectFormByName(self, formname):
        if formname != "":  # Si el id no está vacío
            try:
                self.selectedForm = True
                return self.br.select_form(name=formname)
            except:
                return BR_ERRORxERROR_SET_FORM
        else:
            return BR_ERRORxNO_FORMID

    def submitForm(self, form, values):  # Enviar un formulario
        if self.selectedForm:
            if len(form) > 0 and len(values) > 0:
                if len(form) == len(values):
                    try:
                        for i in range(len(form)):
                            self.br.form[form[i]] = values[i]
                        self.br.submit()
                    except:
                        return BR_ERRORxERROR_SET_SUBMIT
                else:
                    return BR_ERRORxNO_VALID_SUBMIT_NOT_EQUAL
            else:
                return BR_ERRORxNO_VALID_SUBMIT_EMPTY
        else:
            return BR_ERRORxNO_SELECTED_FORM

    def clearCookies(self):  # Elimina las cookies
        self.cookies.clear_session_cookies()


# noinspection PyClassHasNoInit
class color:
    """Clase que permite manejar colores en la terminal"""

    # Si el sistema operativo no es windows entonces los colores se activan
    if os.name != "nt":
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'
    else:
        PURPLE = ''
        CYAN = ''
        DARKCYAN = ''
        BLUE = ''
        GREEN = ''
        YELLOW = ''
        RED = ''
        BOLD = ''
        UNDERLINE = ''
        END = ''
