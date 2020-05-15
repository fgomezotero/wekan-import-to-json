#!/usr/bin/env python3

import argparse

def check_arg():
    """Realiza el parseo de la llamada al CLI

    Returns:
        [tupla] -- [Espacio de nombre de los parámetros pasados al CLI]
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


def main():
    args = check_arg()
    print(args)
    print("Script finalizado..!")

if __name__ == "__main__":
    main()