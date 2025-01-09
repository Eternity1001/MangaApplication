import sqlite3


def create_database():
    
    con = sqlite3.connect("../.venv/Manga.db")
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE Manga (
        Title varchar(500),
        Genre text(1000),
        Thumpnail varchar(500),
        Main varchar(1000),
        Chapter MEDIUMTEXT,
        Read varchar(50)
    )""")
    
    
def get_con() -> sqlite3.Connection:
    con = sqlite3.connect("Manga.db")
    return con


def commit(con: sqlite3.Connection) -> None:
    con.commit()

def insert(title: str, genre: str, thumpnail: str, main: str, chapter: str,  con: sqlite3.Connection, read:str = "0"):
    
    cursor = con.cursor()
    data = (title, genre, thumpnail, main, chapter, read)
    cursor.execute("""INSERT OR REPLACE INTO Manga VALUES (?, ?, ?, ?, ?, ?)""", data)
    commit(con)
    
    
    