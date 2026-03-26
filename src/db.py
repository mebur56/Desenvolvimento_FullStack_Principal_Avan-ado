

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "nobel.db")

#Criação da tabela caso não exista e carga inicial
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table'
          AND name = 'nobel'
        LIMIT 1
    """)

    exists = cursor.fetchone() is not None
    if exists is False:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nobel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                laureateId Integer NOT NULL UNIQUE,
                laureateName VARCHAR(70),
                amount integer,
                motivation VARCHAR(500),
                description VARCHAR(500)
            )
        """)
        conn.commit()

    conn.close()

def get_all_favorites():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM nobel
    """)
    rows = cursor.fetchall() 
    conn.close()  

    favorites = []
    for row in rows:
        favorites.append({
            "id": row[0],
            "laureateId": row[1],
            "laureateName": row[2],
            "amount": row[3],
            "motivation": row[4],
            "description": row[5]

        })
        
    return favorites

def create_favorite(favorite):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print(favorite)
    cursor.execute("""
        INSERT INTO nobel (laureateId, laureateName,amount, motivation, description)
        VALUES (?, ?, ?,?, ?)
    """, (favorite["laureateId"], favorite["laureateName"],favorite["amount"], favorite["motivation"], favorite["description"]))

    conn.commit()
    conn.close()  

def delete_favorite(id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM nobel WHERE ID = ?
    """, (id,))

    conn.commit()
    conn.close()

def update_description(id:int, description: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE nobel
        SET description = ?
        WHERE id =?
    """, (description, id))

    conn.commit()
    conn.close()

def get_favorites_ids():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        select id from nobel
    """, ())

    rows = cursor.fetchall() 
    conn.close()  

    ids = []
    for row in rows:
        ids.append(
            row[0]
        )
    return ids

    
      