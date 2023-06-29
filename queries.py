import sqlite3

# Connecting to the database
conn = sqlite3.connect("slang.db")
cursor = conn.cursor()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> S Q L    S T A T E M E N T S <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Creating Table
try:
    cursor.execute("drop table if exists SlangPanameno")
    cursor.execute("CREATE TABLE SlangPanameno(id Integer PRIMARY KEY, word text, meaning text)")
except sqlite3.OperationalError:
    pass


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
def edit_record(id_requested, word_requested, new_word, new_meaning):
    with conn:
        cursor.execute("UPDATE SlangPanameno SET word=:new_word, meaning=:new_meaning WHERE word = :word_requested or id = :id_requested",
                       {'word_requested': word_requested, 'id_requested': id_requested, 'new_meaning': new_meaning, 'new_word': new_word})


# Delete record (3)
def del_record(value_requested):
    with conn:
        cursor.execute("DELETE FROM SlangPanameno WHERE word=:word or id = :id", {'word': value_requested, 'id': value_requested})


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
