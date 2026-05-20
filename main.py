from database import criar_tabelas
from usuarios import cadastrar_usuario, buscar_usuario_por_email
from categorias import cadastrar_categoria, listar_categorias
from transacoes import cadastrar_transacao, listar_transacoes, deletar_transacao, editar_transacao


usuario_logado = None

def menu_principal():
    print("\n===============================")
    print("     BEM-VINDO AO FINCONTROL   ")
    print("===============================")
    print("1 - Cadastrar usuário")
    print("2 - Fazer login")
    print("0 - Sair")
    return input("Escolha uma opção: ")

def menu_sistema():
    print(f"\n=== OLÁ, {usuario_logado['nome'].upper()}! ===")
    print("1 - Cadastrar categoria")
    print("2 - Listar categorias")
    print("3 - Cadastrar transação")
    print("4 - Listar transações")
    print("5 - Deletar transação")
    print("0 - Sair")
    return input("Escolha uma opção: ")

def fazer_login():
    global usuario_logado
    print("\nLOGIN")
    email = input("Email: ")
    senha = input("Senha: ")

    usuario = buscar_usuario_por_email(email)

    if usuario and usuario["senha"] == senha:
        usuario_logado = usuario
        print(f"Login realizado com sucesso! Bem-vindo, {usuario['nome']}!")
    else:
        print("Email ou senha incorretos!")

def main():
    criar_tabelas()

    while True:
        if usuario_logado is None:
            opcao = menu_principal()

            if opcao == "1":
                print("\n--- CADASTRO DE USUÁRIO ---")
                nome  = input("Nome: ")
                email = input("Email: ")
                senha = input("Senha: ")
                cadastrar_usuario(nome, email, senha)

            elif opcao == "2":
                fazer_login()

            elif opcao == "0":
                print("Encerrando sistema... Até logo!")
                break

            else:
                print("Opção inválida!")

        else:
            opcao = menu_sistema()

            if opcao == "1":
                print("\nCADASTRAR CATEGORIA")
                nome = input("Nome da categoria: ")
                tipo = input("Tipo (receita/despesa): ")
                cadastrar_categoria(nome, tipo)

            elif opcao == "2":
                print("\nCATEGORIAS CADASTRADAS")
                categorias = listar_categorias()
                if categorias:
                    for c in categorias:
                        print(f"[{c['id']}] {c['nome']} - {c['tipo']}")
                else:
                    print("Nenhuma categoria cadastrada ainda.")

            elif opcao == "3":
                print("\nCADASTRAR TRANSAÇÃO")
                categorias = listar_categorias()
                if not categorias:
                    print("Cadastre uma categoria primeiro!")
                else:
                    for c in categorias:
                        print(f"[{c['id']}] {c['nome']} - {c['tipo']}")
                    descricao   = input("Descrição: ")
                    valor       = float(input("Valor: "))
                    data        = input("Data (dd/mm/aaaa): ")
                    tipo        = input("Tipo (receita/despesa): ")
                    id_categoria = int(input("ID da categoria: "))
                    cadastrar_transacao(descricao, valor, data, tipo, usuario_logado["id"], id_categoria)

            elif opcao == "4":
                print("\nSUAS TRANSAÇÕES")
                transacoes = listar_transacoes(usuario_logado["id"])
                if transacoes:
                    for t in transacoes:
                        print(f"[{t['id']}] {t['data']} | {t['descricao']} | R$ {t['valor']:.2f} | {t['tipo']} | {t['categoria']}")
                else:
                    print("Nenhuma transação cadastrada ainda.")

            elif opcao == "5":
                print("\nDELETAR TRANSAÇÃO")
                id_transacao = int(input("ID da transação: "))
                deletar_transacao(id_transacao)

            elif opcao == "0":
                print("Encerrando sistema... Até logo!")
                break

            else:
                print("Opção inválida!")

main()