import sqlite3


DB_NAME = "fincontrol.db"

def get_conexao():
    
    conexao = sqlite3.connect(DB_NAME)
    conexao.row_factory = sqlite3.Row  
    return conexao

def criar_tabelas():
    
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS usuario (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome      TEXT    NOT NULL,
            email     TEXT    NOT NULL UNIQUE,
            senha     TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS categoria (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            nome  TEXT    NOT NULL,
            tipo  TEXT    NOT NULL CHECK(tipo IN ('receita', 'despesa'))
        );

        CREATE TABLE IF NOT EXISTS transacao (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao    TEXT    NOT NULL,
            valor        REAL    NOT NULL,
            data         TEXT    NOT NULL,
            tipo         TEXT    NOT NULL CHECK(tipo IN ('receita', 'despesa')),
            id_usuario   INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL,
            FOREIGN KEY (id_usuario)   REFERENCES usuario(id),
            FOREIGN KEY (id_categoria) REFERENCES categoria(id)
        );
    """)

    conexao.commit()
    conexao.close()
    print("Banco de dados iniciado com sucesso!")

criar_tabelas()