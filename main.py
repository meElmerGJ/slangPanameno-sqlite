"""
    ***UTILIZANDO PYTHON 3.10 ******

    Elaborar una aplicación de línea de comandos en Python que sirva cuyo propósito sea mantener un diccionario de
    palabras del slang panameño (xopa, mopri, otras). Las palabras y su significado deben ser almacenadas dentro de una
    base de datos SQLite. Las opciones dentro del programa deben incluir como mínimo:
        a) Agregar nueva palabra
        b) Editar palabra existente
        c) Eliminar palabra existente
        d) Ver listado de palabras
        e) Buscar significado de palabra
        f) Salir


    Dictionary from: https://es.wiktionary.org/wiki/Wikcionario:Jerga_paname%C3%B1a

"""
from slangPanameno import Slang
from queries import *
# "tabulate" library necessary to view correctly table format
from tabulate import tabulate


# Format output strings
lb = "\n\n"                 # line break
tab = "\t\t"                # tabulation
lb_t = "\n\t\t"             # line break + tabulation
lb_t2 = f"{lb_t}{tab}"      # line break + double tabulation


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> P R O G R A M    F U N C T I O N S <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Adding word function
def add_word():
    word = input(f"{lb_t2}Ingresa la palabra: ")
    meaning = input(f"{lb_t2}Ingresa el significado: ")
    new_word = Slang(word, meaning)
    insert_record(new_word)
    print(f"{lb_t2}¡Palabra guardada!")


# Editing word function
def edit_word():
    value_requested = input(f"{lb_t2}Presiones 0 para ver palabras{lb_t2}Ingrese el numero (#) o la palabra a editar: ")
    if value_requested == "0":
        see_words()
        edit_word()
    else:
        if exist(value_requested):
            new_word = input(f"{lb_t2}Ingrese nueva palabra: ")
            new_meaning = input(f"{lb_t2}Ingrese el significado: ")
            edit_record(value_requested, new_word, new_meaning)
            print(f"{lb_t2}¡Palabra editada!")
        else:
            print(f"{lb_t2}ERROR: El valor ingresado no existe en la base de datos")


# Deleting word function
def del_word():
    word = input(f"{lb_t2}Ingresa palabra para eliminar: ")
    del_record(word)
    print(f"{lb_t2}¡Palabra eliminada!")


# See words function
def see_words():
    table = get_records()
    print(tabulate(table, headers=["#", "PALABRA", "SIGNIFICADO"], tablefmt="psql"))
    input('\n"Enter" para continuar')


# Getting word meaning function
def get_meaning():
    word = input(f"{lb_t}{tab}Ingresa la palabra a buscar: ")
    try:
        x = get_meaning_by_word(word)
        print(f"{lb_t2}{x[1]}, significa: {x[2]}")
    except TypeError:
        print(f"{lb_t2}ERROR - Palabra no encontrada")


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> E N D <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#
#
#
#
#
#
#
#
#


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> P R O G R A M <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
print(f"{lb}BIENVENIDO AL DICCIONARIO DE SLANG PANAMEÑO\n")

# Program menu
menu = """

        
        1) Agregar nueva palabra
        2) Editar palabra
        3) Eliminar palabra 
        4) Ver palabras
        5) Buscar significado de palabra
        6) Salir
        """

# Program main loop // Warning! -> *** Need to use Python 3.10 for match - case Statements ***
end = False

while not end:
    try:
        print(menu)
        option = int(input(f"{lb_t}Ingresa una opcion: "))
        match option:
            case 1:
                add_word()
            case 2:
                edit_word()
            case 3:
                del_word()
            case 4:
                see_words()
            case 5:
                get_meaning()
            case 6:
                exit(0)
    except ValueError:
        print(f"{lb_t}ERROR - Ingrese una opcion correcta")
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> E N D <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# Closing connection
conn.close()
