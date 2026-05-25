from database import get_conexao

def cadastrar_transacao(descricao, valor, data, tipo, id_usuario, id_categoria):
    

    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO transacao (descricao, valor, data, tipo, id_usuario, id_categoria)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (descricao, valor, data, tipo, id_usuario, id_categoria))

    conexao.commit()
    conexao.close()
    print(f"Transação '{descricao}' cadastrada com sucesso!")


def listar_transacoes(id_usuario):
  
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT t.id, t.descricao, t.valor, t.data, t.tipo, c.nome AS categoria
        FROM transacao t
        JOIN categoria c ON t.id_categoria = c.id
        WHERE t.id_usuario = ?
        ORDER BY t.data DESC
    """, (id_usuario,))

    transacoes = cursor.fetchall()
    conexao.close()
    return transacoes


def deletar_transacao(id_transacao):
    
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM transacao WHERE id = ?", (id_transacao,))

    conexao.commit()
    conexao.close()
    print("Transação deletada com sucesso!")
    

def editar_transacao(id_transacao, descricao, valor, data, tipo, id_categoria):
    
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE transacao
        SET descricao = ?, valor = ?, data = ?, tipo = ?, id_categoria = ?
        WHERE id = ?
    """, (descricao, valor, data, tipo, id_categoria, id_transacao))

    conexao.commit()
    conexao.close()
    print("Transação atualizada com sucesso!")


    def buscar_transacao_por_nome(descricao, id_usuario):
        conexao = get_conexao()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT t.id, t.descricao, t.valor, t.data, t.tipo, c.nome AS categoria
            FROM transacao t
            JOIN categoria c ON t.id_categoria = c.id
            WHERE t.id_usuario = ?
            AND t.descricao LIKE ?
            ORDER BY t.data DESC
        """, (id_usuario, f"%{descricao}%"))

        transacoes = cursor.fetchall()
        conexao.close()
        return transacoes