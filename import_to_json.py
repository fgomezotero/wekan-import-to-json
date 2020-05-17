#!/usr/bin/env python3

import argparse
import json

from io import *
from termcolor import colored, cprint

def check_arg():
    """Realiza el parseo de la llamada al CLI

    Returns:
        namespace -- [Espacio de nombre de los parámetros pasados al CLI]
    """
    parse = argparse.ArgumentParser(prog='import-to-json',
                                    usage='%(prog)s [-h|--help] -e|--excel file.xls -j|--json input.json -s|--swimlane name [-o|--output output.json]',
                                    description='Añadir tarjetas leídas desde un archivo externo a un fichero JSON exportado de Wekan',
                                    epilog='',
                                    allow_abbrev=False)
    parse.add_argument('-f','--file',
                        type=str,
                        help='Fichero desde donde se cargan las nuevas tarjetas',
                        required=True)    
                        
    parse.add_argument('-j','--json',
                        type=str,
                        help='JSON exportado desde Wekan',
                        required=True)    
                        
    parse.add_argument('-s','--swimlane',
                        type=str,
                        help='Swimlane contenedor de las tarjetas creadas',
                        required=True)

    parse.add_argument('-o','--output',
                        help='(Opcional) JSON final con las tarjetas cargadas',
                        type=str)

    args = parse.parse_args()
    return args


def load_json(file):
    """Leer la información del archivo .json

    Arguments:
        file {str} -- Nombre o path del archivo json exportado de wekan

    Returns:
        dict -- Diccionario correspondiente al contenido del archivo json
    """
    with open(file, 'r') as filePointer:
        context = filePointer.read()
        jsonText = json.loads(context)
        filePointer.close()

    return jsonText


def json_summary(jsonDict):
    """Imprimir el resumen de la información cargado del archivo json

    Arguments:
        jsonDict {dict} -- Diccionario correspondiente al contenido del archivo json
    """
    cprint('\n¡JSON importado correctamente!', 'green', 'on_white',attrs=['bold'])
    print ("Resumen:")
    print ("\tNombre del tablero: ", jsonDict['title'])
    print ("\tCantidad de listas: ", len(jsonDict['lists']))
    print ("\tCantidad de usuarios: ", len(jsonDict['users']))
    print ("\tCantidad de swimlanes: ", len(jsonDict['swimlanes']))
    print ("\tCantidad de tarjetas: ", len(jsonDict['cards']))


def write_json(file, jsonDict):
    """Escribiendo el json modificado para el archivo pasado como parámetro a la CLI

    Arguments:
        file {str} -- Nombre o path del archivo json final
        jsonDict {dict} -- Diccionario correspondiente al contenido del archivo json
    """
    with open(file,'w') as filePointer:
        filePointer.write(json.dumps(jsonDict, ensure_ascii=False))
        filePointer.close()


def main():
    """Función que orquesta el script
    """
    error = False
    try:
        args = check_arg() # Comprabamos que los parámetros están correctos
        jsonText = load_json(args.json) # Cargamos el archivos .json
        json_summary(jsonText) # Mostramos el resumen de la carga del archivo json
        if args.output == None: 
            print(json.dumps(jsonText, ensure_ascii=False, indent=4)) # Imprimimos en stdout el json transformado
        else:
            write_json(args.output, jsonText) # Escribiendo el json modificado para el archivo pasado como parámetro a la CLI

    except FileNotFoundError:
        print ("Error: Archivo {} no se encuentra".format(args.json))
        error = True
    except PermissionError:
        cprint ("Permiso denegado: No tiene permiso para crear el archivo {}".format(args.output), 'red', attrs=['bold'])
        error = True
    finally:
        if error:
            cprint("¡Programa finalizado con errores!",'red','on_white',attrs=['bold'])
        else:
            cprint("¡Programa finalizado satsfactoriamente!",'green','on_white',attrs=['bold'])


if __name__ == "__main__":
    main()