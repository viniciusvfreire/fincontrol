from database import get_conexao

def cadastrar_usuario(nome, email, senha):
   
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO usuario (nome, email, senha)
        VALUES (?, ?, ?)
    """, (nome, email, senha))

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

