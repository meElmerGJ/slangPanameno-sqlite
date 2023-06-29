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
import sqlite3

# "tabulate" library necessary to view correctly table format
from tabulate import tabulate


# Class Slang , used to create new words
class Slang:
    def __init__(self, word, meaning):
        self.id = None
        self.word = word
        self.meaning = meaning


# Format output strings
lb = "\n\n"
tab = "\t\t"
lb_t = "\n\t\t"
lb_t2 = f"{lb_t}{tab}"

# Connecting to the database
conn = sqlite3.connect("slang.db")
cursor = conn.cursor()

# Creating Table
try:
    cursor.execute("drop table if exists SlangPanameno")
    cursor.execute("CREATE TABLE SlangPanameno(id Integer PRIMARY KEY, word text, meaning text)")
except sqlite3.OperationalError:
    pass


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> S Q L    S T A T E M E N T S <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Insert new record (1)
def insert_record(slang):
    with conn:
        cursor.execute("INSERT INTO SlangPanameno VALUES (:id, :word, :meaning)",
                       {'id': slang.id, 'word': slang.word, 'meaning': slang.meaning})


def exist(value_requested):
    with conn:
        cursor.execute("SELECT id or word from SlangPanameno WHERE id = :id or word = :word",
                       {'id': value_requested, 'word': value_requested})
        result = cursor.fetchone()
        if result is None:
            return False
        else:
            return True


# Edit records (2)
def edit_record(word_request, new_word, new_meaning):
    with conn:
        cursor.execute("UPDATE SlangPanameno SET word=:new_word, meaning=:new_meaning WHERE word = :word_request or id = :word_request ",
                   {'word_request': word_request, 'new_meaning': new_meaning, 'new_word': new_word})


# Delete record (3)
def del_record(word):
    with conn:
        cursor.execute("DELETE FROM SlangPanameno WHERE word=:word", {'word': word})


# Show all records (4)
def get_records():
    with conn:
        cursor.execute("SELECT * FROM SlangPanameno")
        return cursor.fetchall()


# Search a specific word meaning (5)
def get_meaning_by_word(word):
    cursor.execute("SELECT * FROM SlangPanameno WHERE word=:word", {'word': word})
    result = cursor.fetchone()
    return result


# INSERTING RECORDS TO TEST THE PROJECT
cursor.execute("""
            insert into SlangPanameno(word, meaning)
            values 
              ('Chombo', 'Se usa para referirse a los afroantillanos y sus descendientes'),
              ('Jato', 'Casa o hogar'),
              ('Pana', 'Amigo o camarada'),
              ('Que xopa!', 'El clasico saludo de nosotros'),
              ('Taquilla', 'Alguna historia o relato que puede ser falsa'),
              ('Quilla', 'Dinero'),
              ('Tirar la posta', 'Contar una historia o chisme'),
              ('Taquear', 'Comer en exceso'),
              ('Chiri', 'Frío'),
              ('Pelea de gallos', 'Competencia o disputa acalorada');
            """)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> E N D <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#
#
#
#


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
