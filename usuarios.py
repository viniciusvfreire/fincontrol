import bcrypt
from database import get_conexao

def cadastrar_usuario(nome, email, senha):
    conexao = get_conexao()
    cursor = conexao.cursor()

    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    cursor.execute("""
        INSERT INTO usuario (nome, email, senha)
        VALUES (?, ?, ?)
    """, (nome, email, senha_hash))

    conexao.commit()
    conexao.close()
    print(f"Usuário {nome} cadastrado com sucesso!")

def buscar_usuario_por_email(email):
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM usuario WHERE email = ?
    """, (email,))

    usuario = cursor.fetchone()
    conexao.close()
    return usuario

def verificar_senha(senha, senha_hash):
    return bcrypt.checkpw(senha.encode('utf-8'), senha_hash)

