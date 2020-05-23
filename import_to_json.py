#!/usr/bin/env python3

import argparse
import json

from io import *
from termcolor import colored, cprint

def check_arguments():
    """Parse the call to the CLI

    Returns:
        namespace -- [Namespaces for all the parameters passed to the CLI]
    """
    parse = argparse.ArgumentParser(prog='import-to-json',
                                    usage='%(prog)s [-h|--help] -e|--excel file.xls -j|--json input.json -s|--swimlane name [-o|--output output.json]',
                                    description='Add cards read from an external file to a JSON file exported from Wekan',
                                    epilog='',
                                    allow_abbrev=False)
    parse.add_argument('-f','--file',
                        type=str,
                        help='File from where new cards are loaded',
                        required=True)    
                        
    parse.add_argument('-j','--json',
                        type=str,
                        help='JSON file exported from Wekan',
                        required=True)    
                        
    parse.add_argument('-s','--swimlane',
                        type=str,
                        help='Swimlane containing all imported cards, which may or not may exist',
                        required=True)

    parse.add_argument('-o','--output',
                        help='(Optional) Final JSON with all cards joined from both files',
                        type=str)

    args = parse.parse_args()
    return args


def load_from_json(file):
    """Read and load the json file context

    Arguments:
        file {str} -- Absolute or relative path to json file exported from Wekan

    Returns:
        dict -- Data structure corresponding to the content of the json file
    """
    with open(file, 'r') as filePointer:
        context = filePointer.read()
        jsonText = json.loads(context)
        filePointer.close()

    return jsonText


def json_summary(jsonDict):
    """Prints a summary content of the json file loaded 

    Arguments:
        jsonDict {dict} -- Dictionary corresponding to the content of the json file
    """
    cprint('\nThe json file have been imported correctly!', 'green', 'on_white',attrs=['bold'])
    print ("Brief summary:")
    print ("\tBoard imported: ", jsonDict['title'])
    print ("\tTotal quantity of lists imported: ", len(jsonDict['lists']))
    print ("\tTotal quantity of users imported: ", len(jsonDict['users']))
    print ("\tTotal quantity of swimlanes imported: ", len(jsonDict['swimlanes']))
    print ("\tTotal quantity of cards imported: ", len(jsonDict['cards']))


def write_to_json(file, jsonDict):
    """Writing a dictionary to a json file

    Arguments:
        file {str} -- Absolute or relative path to the json file
        jsonDict {dict} -- Dictionary with the information to save in the json file
    """
    with open(file,'w') as filePointer:
        filePointer.write(json.dumps(jsonDict, ensure_ascii=False))
        filePointer.close()


def there_is_user(user_slug):
    pass


def there_is_swimlane(swimlane_slug):
    pass


def main():
    """Main function which orchestrate the script
    """
    error = False
    try:
        args = check_arguments() # Checking that all needed parameters are right
        jsonText = load_from_json(args.json) # Loading the json file
        json_summary(jsonText) # Printing a summary of the json file loaded previously

        if args.output == None: 
            print(json.dumps(jsonText, ensure_ascii=False, indent=4)) # Print to stdout the final JSON   
        else:
            write_to_json(args.output, jsonText) # Write to a Json file the result

    except FileNotFoundError:
        print ("Error: Json file {} not found".format(args.json))
        error = True
    except PermissionError:
        cprint ("Denied permission: Do not have permission to create a json file: {}".format(args.output), 'red', attrs=['bold'])
        error = True
    finally:
        if error:
            cprint("Script execution ends with error!",'red','on_white',attrs=['bold'])


if __name__ == "__main__":
    main()