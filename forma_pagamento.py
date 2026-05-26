from database import get_conexao

def cadastrar_forma_pagamento(nome):
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO forma_pagamento (nome)
        VALUES (?)
    """, (nome,))

    conexao.commit()
    conexao.close()
    print(f"Forma de pagamento '{nome}' cadastrada com sucesso!")

def listar_formas_pagamento():
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM forma_pagamento")

    formas = cursor.fetchall()
    conexao.close()
    return formas

def editar_forma_pagamento(id, nome):
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE forma_pagamento
        SET nome = ?
        WHERE id = ?
    """, (nome, id))

    conexao.commit()
    conexao.close()
    print("Forma de pagamento atualizada com sucesso!")

def deletar_forma_pagamento(id):
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM forma_pagamento WHERE id = ?", (id,))

    conexao.commit()
    conexao.close()
    print("Forma de pagamento deletada com sucesso!")