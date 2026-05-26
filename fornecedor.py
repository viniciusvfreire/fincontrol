from database import get_conexao

def cadastrar_fornecedor(nome, cnpj, telefone):
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO fornecedor (nome, cnpj, telefone)
        VALUES (?, ?, ?)
    """, (nome, cnpj, telefone))

    conexao.commit()
    conexao.close()
    print(f"Fornecedor '{nome}' cadastrado com sucesso!")

def listar_fornecedores():
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM fornecedor")

    fornecedores = cursor.fetchall()
    conexao.close()
    return fornecedores

def buscar_fornecedor_por_id(id):
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM fornecedor WHERE id = ?", (id,))

    fornecedor = cursor.fetchone()
    conexao.close()
    return fornecedor

def editar_fornecedor(id, nome, cnpj, telefone):
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE fornecedor
        SET nome = ?, cnpj = ?, telefone = ?
        WHERE id = ?
    """, (nome, cnpj, telefone, id))

    conexao.commit()
    conexao.close()
    print("Fornecedor atualizado com sucesso!")

def deletar_fornecedor(id):
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM fornecedor WHERE id = ?", (id,))

    conexao.commit()
    conexao.close()
    print("Fornecedor deletado com sucesso!")