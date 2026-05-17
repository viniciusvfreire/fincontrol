from database import get_conexao


def cadastrar_categoria(nome, tipo):
    
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO categoria (nome, tipo)
        VALUES (?, ?)
    """, (nome, tipo))

    conexao.commit()
    conexao.close()
    print(f"Categoria '{nome}' cadastrada com sucesso!")


def listar_categorias():
    
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM categoria")

    categorias = cursor.fetchall()
    conexao.close()
    return categorias


def buscar_categoria_por_id(id):
    
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM categoria WHERE id = ?", (id,))

    categoria = cursor.fetchone()
    conexao.close()
    return categoria