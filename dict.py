#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Multi-diccionario online

# DICT
# Autor: PABLO PIZARRO @ ppizarro
# Fecha: JUNIO 2015
# Licencia: CC BY-NC 4.0

# Importación de liberías
from utils import *


# Definicion de constantes
global source
DEFAULT_LOOK = getConfigValue("source.defaults", True)
DICTIONARIES = ["[Urban Dictionary]", "[WordReference Español]", "[WordReference Inglés]",
                "[WordReference Sinónimos Español]", \
                "[WordReference Sinónimos Inglés]"]
REPLACE_ALL = 0x01
REPLACE_ALPHA = 0x04
REPLACE_NUMBER = 0X03
REPLACE_SYMBOL = 0X02
REPLACE_SYMBOL_SIMPLE = 0x05
RESULT_COLORED = getConfigValue("results.color")
RESULT_LINES_SEP = int(getConfigValue("result.lines.separation"))
RESULT_SORT = getConfigValue("results.sort")
RESULT_TITLE_BOLD = getConfigValue("result.title.bold")
RESULT_TITLE_UPPER = getConfigValue("result.title.upper")
SPACE = 3
CHARS = {
    REPLACE_ALL: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;?@[\\]^_`{|}~',
    REPLACE_ALPHA: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
    REPLACE_NUMBER: '0123456789',
    REPLACE_SYMBOL: '!"#$%&\'()*+,-./:;?@[\\]^_`{|}~',
    REPLACE_SYMBOL_SIMPLE: '.-) :'}
SEPARATOR = '<new>'
VERSION = "1.4"
CONFIG_DICT_FILE = 'dict.configs'

# Se aplican configuraciones
if not RESULT_COLORED:
    # noinspection PyClassHasNoInit
    class color:
        """Desactiva los colores"""
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

# Funciones de usuario
def getDictName(index):
    """Retorna el nombre de diccionario index"""
    return DICTIONARIES[index].replace("[", "").replace("]", "")


def printHelp():
    """Imprime la ayuda y cierra la aplicacion"""

    def printSourceConfig(name, descr):
        """Imprime un source"""
        if DEFAULT_LOOK == name:
            print delAcents("\t\t{0}\t{1} ".format(name, descr) + color.BOLD + "(default)" + color.END + ".")
        else:
            print delAcents("\t\t{0}\t{1}.".format(name, descr))

    print color.BOLD + "NOMBRE" + color.END
    print "\tdict -- Dictionary\n"
    print color.BOLD + "SINOPSIS" + color.END
    print "\t" + color.BOLD + "dict" + color.END + "\t[word <source>] ['phrase' <source>]\n\t\t[--help] [--version] [--about]\n\t\t[--config <name> <param>]\n"
    print delAcents(color.BOLD + "DESCRIPCIÓN" + color.END)
    print delAcents("\tDict permite buscar la definición de palabras en múltiples fuentes de forma rápida.")
    print "\ty segura.\n"
    print color.BOLD + "COMANDOS" + color.END
    print delAcents("\tword, 'phrase' <source>\n\t\tBusca la palabra " + color.BOLD + "word" + color.END + \
                    " de forma online en distintas fuentes especificadas en \n\t\tsource. Para buscar una palabra compuesta (" + color.BOLD + "phrase" + color.END + "), es necesario usar comillas\n\t\tsimples o dobles, por ejemplo, " + color.BOLD + "'" + color.END + "dict foo" + color.BOLD + "'" + color.END + ".\n\t\tLas fuentes pueden ser definidas usando los siguientes argumentos:\n")
    printSourceConfig("-a", "Buscar en todas las fuentes disponibles")
    printSourceConfig("-en", "Buscar en {0}".format(getDictName(2)))
    printSourceConfig("-es", "Buscar en {0}".format(getDictName(1)))
    printSourceConfig("-ses", "Buscar en {0}".format(getDictName(3)))
    printSourceConfig("-u", "Buscar en {0}".format(getDictName(0)))
    print ""
    print color.BOLD + "OPCIONES" + color.END
    print delAcents("\t--about, -ab\n\t\tImprime la información de autor de este programa.\n")
    print delAcents(
        "\t--config, -c <name> <param>\n\t\tDefine el archivo de configuración <name> con el valor <param>.\n")
    print "\t--help, -h\n\t\tDespliega esta ayuda.\n"
    print delAcents("\t--version, -v\n\t\tImprime la versión del programa.\n")
    print "\n" + color.BOLD + "CONFIGURACIONES" + color.END
    confs = os.listdir(CONFIG_FOLDER)
    try:
        confs.remove(".empty")
    except:
        pass
    confs.sort()
    maxsep = 0
    avconf = loadConfigFile(CONFIG_DICT_FILE).split("\n")
    for f in confs:
        maxsep = max(maxsep, len(f))
    maxsep += 5
    for f in confs:
        for j in avconf:
            if f==j:
                print "\t{0}{1}".format(f.ljust(maxsep), getConfigValue(f, True, True))
                break
    print "\n" + color.BOLD + "AUTOR" + color.END
    print "\tPablo Pizarro, ver en " + color.UNDERLINE + "https://ppizarror.com" + color.END
    print ""
    exit()


def printUsage():
    """Imprime el uso de la aplicacion"""
    print "uso: " + color.BOLD + "dict" + color.END + " [word <source>] ['phrase' <source>]\n\t  [--help] [--version] [--about]\n\t  [--config <name> <param>]"
    exit()


def lookSource():
    """Busca la fuente en los argumentos"""
    if len(sys.argv) > 2:
        arg = sys.argv[2].strip().upper()
    else:
        arg = DEFAULT_LOOK
    if arg == "-A":
        return "all"
    elif arg == "-U":
        return DICTIONARIES[0]
    elif arg == "-ES":
        return DICTIONARIES[1]
    elif arg == "-EN":
        return DICTIONARIES[2]
    elif arg == "-SES":
        return DICTIONARIES[3]
    else:
        error("Fuente desconocida", True)


def lookArguments():
    """Busca posibles argumentos"""
    arg = sys.argv[1]
    if arg == "--help" or arg == "-h":
        printHelp()
    elif arg == "--about" or arg == "-ab":
        print "Autor: Pablo Pizarro"
        print "Fecha: Junio del 2015"
        print "Licencia: CC BY-SA 4.0"
    elif arg == "--version" or arg == "-v":
        print VERSION
    elif arg == "--config" or arg == "-c":
        if len(sys.argv) > 3:
            name = sys.argv[2]
            value = sys.argv[3]
            if name != "":
                if value != "":
                    setConfig(name, value)
                    addLineConfigFile(CONFIG_DICT_FILE, name)
                else:
                    error("Valor de configuración inválido")
            else:
                error("Nombre de configuración inválido")
        else:
            error("config: argumentos insuficientes")
    else:
        error("Argumento desconocido")
    exit()


def replace(string, old, new, tipo=REPLACE_ALL):
    """Funcion que reemplaza strings con regex unico"""
    string = str(string)
    if "*" in old:
        if tipo in CHARS.keys():
            for char in CHARS[tipo]:
                string = string.replace(old.replace("*", char), new)
            return string
        else:
            raise Exception("tipo invaido")
    else:
        return string.replace(old, new)


def getSource(index):
    """Retorna si la fuente de busquea fue seleccionada o no"""
    if index <= len(DICTIONARIES):
        if (source == "all") or (source == DICTIONARIES[index]):
            return True
    return False


if __name__ == "__main__":
    """Se ejecuta la aplicacion"""

    # Se borra el cache
    cleanConfigDir()

    # Se crea el browser
    try:
        browser = Browser()
        browser.addHeaders(HREF_HEADERS)
    except:
        error("Error al crear el navegador interno", True)

    # Se obtiene el input de usuario
    if len(sys.argv) == 1:
        printUsage()

    word = sys.argv[1].replace(" ", "+")
    if "-" in word:  # Formato de argumento
        lookArguments()
    word = word.replace("'", "").replace("'", "")
    source = lookSource()
    definitions = {}

    # Busqueda en urbandictionary
    if getSource(0):
        try:
            browser.abrirLink("http://www.urbandictionary.com/define.php?term={0}".format(word))
            if browser.getHtml() == BR_ERRORxNO_OPENED:
                raise Exception()
            else:
                content = browser.getHtml()
                if "Can you define it?" not in content:
                    query = delAcents(unescape(" ".join(
                        getBetween(content, "<div class='meaning'>", '</div>').replace("<br>", "").replace("<br/>",
                                                                                                           "").split())))
                    examples = delAcents(unescape(" ".join(
                        getBetween(content, "<div class='example'>", '</div>').replace("<br>", "").replace("<br/>",
                                                                                                           "").split())))
                    for i in range(9):
                        query = replace(query, "({0}*".format(i), SEPARATOR, REPLACE_SYMBOL_SIMPLE)
                        examples = replace(examples, "({0}*".format(i), SEPARATOR, REPLACE_SYMBOL_SIMPLE)
                        query = replace(query, "{0}*".format(i), SEPARATOR, REPLACE_SYMBOL_SIMPLE)
                        examples = replace(examples, "{0}*".format(i), SEPARATOR, REPLACE_SYMBOL_SIMPLE)
                    query = query.split(SEPARATOR)
                    examples = examples.split(SEPARATOR)
                    result = []
                    counter = 1
                    excounter = 0
                    if examples[0] == "": excounter += 1
                    for line in query:
                        line = str(line).strip()
                        if line != "":
                            if counter > 9:
                                l = 1
                            else:
                                l = 0
                            while '<a href="/define.php?' in line:
                                boldline = getWithTags(line, '<a href="/define.php?', '</a')
                                boldword = getBetweenTags(boldline, '<a', '</a>').strip()
                                line = line.replace(boldline, color.BOLD + boldword + color.END)
                            result.append(" " * (SPACE - l) + "({0}) ".format(counter) + line.capitalize())
                            if excounter < len(examples):
                                ex = examples[excounter]
                                while '<a href="/define.php?' in ex:
                                    boldline = getWithTags(ex, '<a href="/define.php?', '</a')
                                    boldword = getBetweenTags(boldline, '<a', '</a>').strip()
                                    ex = ex.replace(boldline, color.BOLD + boldword + color.END + color.BLUE)
                                ex = ex.replace("<a>", "").replace("<A>", "")
                                result.append("\t" + color.BLUE + ex.capitalize() + color.END)
                            counter += 1
                            excounter += 1
                    if len(result) > 0:
                        definitions[DICTIONARIES[0]] = result
        except:
            error("Error al buscar en la fuente: {0}".format(getDictName(0)))

    # Busqueda en WordReference es
    if getSource(1):
        try:
            browser.abrirLink("http://www.wordreference.com/definicion/{0}".format(word.replace("+", "%20")))
            if browser.getHtml() == BR_ERRORxNO_OPENED:
                raise Exception()
            else:
                content = browser.getHtml()
                if "No se ha encontrado una" not in content:
                    query = delAcents(unescape(getBetween(content, '<div id="article">', '</div'))).split("<li>")
                    new_query = []
                    for l in range(len(query)):
                        if l > 0:
                            new_query.append(query[l].replace("<ol>", "").replace("</ol>", "").split("<br>"))
                    result = []
                    for i in range(len(new_query)):
                        definition = delAcents(unescape(new_query[i][0])).strip().replace("</span>", color.END)
                        if "<span class=ac>" in definition:
                            definition = definition.replace("<span class=ac>", color.RED)
                        if "<span class=b>" in definition:
                            definition = definition.replace("<span class=b>", color.BOLD)
                        if "<span class=i>" in definition:
                            definition = definition.replace("<span class=i>", color.BLUE)
                        definition = definition.replace(":", ".").replace("..", ".")
                        l = 0
                        if i > 8: l = 1
                        definition = " " * (SPACE - l) + "({0}) ".format(i + 1) + definition.capitalize()
                        result.append(definition)
                        if len(new_query[i]) > 1:
                            example = delAcents(unescape(new_query[i][1])).strip()
                            example = example.replace("<span class=i>", "").replace("</span>", "")
                            example = example.capitalize()
                            example = "\t" + color.BLUE + example + color.END
                            result.append(example)
                    if len(result) > 0:
                        definitions[DICTIONARIES[1]] = result
        except:
            error("Error al buscar en la fuente: {0}".format(getDictName(1)))

    # Busqueda en WordReference en
    if getSource(2):
        try:
            browser.abrirLink("http://www.wordreference.com/definition/{0}".format(word.replace("+", "%20")))
            if browser.getHtml() == BR_ERRORxNO_OPENED:
                raise Exception()
            else:
                content = browser.getHtml()
                if "No dictionary entry found for" not in content:
                    query = delAcents(unescape(getBetween(content, '<div id="article">', '</div'))).split("<li>")
                    result = []
                    counter = 1
                    for line in query:
                        if "<span class='rh_empos'>" in line:
                            title = getBetweenTags(line, "<span class='rh_empos'>", "</span")
                            result.append(color.BOLD + title.strip().upper() + color.END)
                        line = line.replace("<span>]</span>", "").replace("<span>[</span>", "")
                        line = line.replace("<span class='rh_txt'>+</span>", "")
                        while True:
                            rhlab = getWithTags(line, "<span class='rh_lab'>", "</span>")
                            if str(rhlab).isdigit():
                                break
                            else:
                                line = line.replace(rhlab, "")
                        subtipe = getWithTags(line, "<span class='rh_cat'>", "</span>")
                        if not str(subtipe).isdigit():
                            line = line.replace(subtipe,
                                                "[" + color.BOLD + getBetweenTags(subtipe, "<span class='rh_cat'>",
                                                                                  "</span>").strip().capitalize() + color.END + "] ")
                        definition = str(getBetweenTags(line, "<span class='rh_def'>", "span")).strip()
                        if (not definition.isdigit()) and len(definition) > 1:
                            definition = definition.replace("<b>", color.BOLD).replace("</b>", color.END)
                            definition = definition.replace("</", "").replace("<", "").replace("  ", " ").replace(":",
                                                                                                                  ".")
                            l = 0
                            if counter > 9: l = 1
                            definition = definition.replace("[ i>~ i>", "").replace(";br>", ";")
                            definition = definition.replace("i>", "").replace("", "")
                            definition = " " * (SPACE - l) + "({0}) ".format(counter) + definition.strip().capitalize()
                            example = str(getBetweenTags(line, "<span class='rh_ex'>", "span"))
                            counter += 1
                            result.append(definition)
                            if not example.isdigit() and len(example) > 1:
                                example = example.replace("</", "").replace("<", "").replace("  ", " ")
                                example = "\t" + color.END + color.BLUE + example.capitalize() + color.END
                                result.append(example)
                    if len(result) > 0:
                        definitions[DICTIONARIES[2]] = result
        except:
            error("Error al buscar en la fuente: {0}".format(getDictName(2)))

    # Busqueda en WordReference sinonimos es
    if getSource(3):
        try:
            browser.abrirLink("http://www.wordreference.com/sinonimos/{0}".format(word.replace("+", "%20")))
            if browser.getHtml() == BR_ERRORxNO_OPENED:
                raise Exception()
            else:
                content = browser.getHtml()
                if "No se ha encontrado" not in content:
                    query = delAcents(unescape(getBetween(content, '<div id="article">', '</div'))).split("<li>")
                    counter = 0
                    result = []
                    for line in query:
                        if counter > 0:
                            if counter > 9:
                                l = 1
                            else:
                                l = 0
                            line = unescape(line).replace("</li>", "").replace("<br>", "").replace("</ul>",
                                                                                                   "")
                            line = line.replace("<ul>", "")
                            if "<span class=r>" not in line:
                                result.append(
                                    " " * (SPACE - l) + "({0}) ".format(counter) + line.strip().capitalize() + ".")
                                counter += 1
                            else:
                                line = line.replace("<span class=r>", color.RED).replace("</span>", color.END)
                                result.append("\t" + line.capitalize() + color.RED + "." + color.END)
                        counter = max(counter, 1)
                    if len(result) > 0:
                        definitions[DICTIONARIES[3]] = result
        except:
            error("Error al buscar en la fuente: {0}".format(getDictName(3)))


    # Imprime los resultados
    keys = definitions.keys()
    if RESULT_SORT:
        keys.sort()
    if len(keys) == 0:
        error("No se han obtenido resultados")
    else:
        for key in keys:
            tit = delAcents(key)
            if RESULT_TITLE_UPPER:
                tit = upperAcents(tit.upper())
            if RESULT_TITLE_BOLD:
                tit = color.BOLD + tit + color.END
            print tit
            for line in definitions[key]:
                print line
            if RESULT_LINES_SEP > 0:
                print "\n" * (RESULT_LINES_SEP - 1)
