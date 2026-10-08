import sqlite3
import os
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS prediction (id INTEGER PRIMARY KEY AUTOINCREMENT, owner_id INTEGER NOT NULL, input_text TEXT NOT NULL, result TEXT NOT NULL, FOREIGN KEY (owner_id) REFERENCES user (id))''')

    cursor.execute("DELETE FROM prediction")
    cursor.execute("DELETE FROM user")

    hash1, hash2 = pwd_context.hash("senha123"), pwd_context.hash("senha456")
    
    cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", ("user1", hash1))
    user1_id = cursor.lastrowid
    
    cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", ("user2", hash2))
    user2_id = cursor.lastrowid

    cursor.execute("INSERT INTO prediction (owner_id, input_text, result) VALUES (?, ?, ?)", (user1_id, "Ticket login", "Alta Prioridade"))
    cursor.execute("INSERT INTO prediction (owner_id, input_text, result) VALUES (?, ?, ?)", (user2_id, "Ticket fatura", "Baixa Prioridade"))

    conn.commit()
    conn.close()
    print("Banco de dados SQLite populado com sucesso em fastapi/database.db!")

if __name__ == "__main__":
    init_db()