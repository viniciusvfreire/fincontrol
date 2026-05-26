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

    CREATE TABLE IF NOT EXISTS fornecedor (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        nome     TEXT    NOT NULL,
        cnpj     TEXT,
        telefone TEXT
    );

    CREATE TABLE IF NOT EXISTS forma_pagamento (
        id   INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS transacao (
        id                 INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao          TEXT    NOT NULL,
        valor              REAL    NOT NULL,
        data               TEXT    NOT NULL,
        tipo               TEXT    NOT NULL CHECK(tipo IN ('receita', 'despesa')),
        id_usuario         INTEGER NOT NULL,
        id_categoria       INTEGER NOT NULL,
        id_fornecedor      INTEGER,
        id_forma_pagamento INTEGER,
        FOREIGN KEY (id_usuario)         REFERENCES usuario(id),
        FOREIGN KEY (id_categoria)       REFERENCES categoria(id),
        FOREIGN KEY (id_fornecedor)      REFERENCES fornecedor(id),
        FOREIGN KEY (id_forma_pagamento) REFERENCES forma_pagamento(id)
    );
""")

    conexao.commit()
    cursor.executescript("""
    INSERT OR IGNORE INTO categoria (id, nome, tipo) VALUES 
    (1, 'Alimentação', 'despesa'),
    (2, 'Transporte', 'despesa'),
    (3, 'Energia', 'despesa'),
    (4, 'Aluguel', 'despesa'),
    (5, 'Salário', 'receita'),
    (6, 'Outros', 'despesa');
""")

    conexao.commit()
    conexao.close()
    print("Banco de dados iniciado com sucesso!")