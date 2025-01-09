import sqlite3


def create_database():
    
    con = sqlite3.connect("../.venv/manga.db")
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE Manga (
        Title varchar(500),
        Genre text(1000),
        Thumpnail varchar(500),
        Main varchar(1000),
        Chapter MEDIUMTEXT,
        Read varchar(50)
    )""")
    
    
def get_con():
    ""

