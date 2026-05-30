import time
import sys
import msvcrt
from database import criar_tabelas
from usuarios import cadastrar_usuario, buscar_usuario_por_email, verificar_senha
from categorias import listar_categorias
from transacoes import cadastrar_transacao, listar_transacoes, deletar_transacao, editar_transacao, buscar_transacao_por_nome
from fornecedor import cadastrar_fornecedor, listar_fornecedores, editar_fornecedor, deletar_fornecedor
from forma_pagamento import cadastrar_forma_pagamento, listar_formas_pagamento, editar_forma_pagamento, deletar_forma_pagamento

def input_senha(prompt="Senha: "):
    print(prompt, end="", flush=True)
    senha = ""
    while True:
        c = msvcrt.getwch()
        if c in ("\r", "\n"):
            print()
            break
        elif c == "\b":
            if senha:
                senha = senha[:-1]
                sys.stdout.write("\b \b")
                sys.stdout.flush()
        else:
            senha += c
            sys.stdout.write("*")
            sys.stdout.flush()
    return senha

def validar_email(email):
    return "@" in email and "." in email

usuario_logado = None

def menu_principal():
    print("\n=============================")
    print("      BEM-VINDO AO FINCONTROL")
    print("=============================")
    print("1 - Cadastrar usuário")
    print("2 - Fazer login")
    print("0 - Sair")
    return input("Escolha: ")

def menu_sistema():
    print(f"\n=== OLÁ, {usuario_logado['nome'].upper()}! ===")
    print("1 - Transações")
    print("2 - Fornecedores")
    print("3 - Formas de pagamento")
    print("0 - Sair")
    return input("Escolha: ")

def submenu_transacoes():
    print("\n--- TRANSAÇÕES ---")
    print("1 - Cadastrar transação")
    print("2 - Listar transações")
    print("3 - Buscar transação por nome")
    print("4 - Deletar transação")
    print("0 - Voltar")
    return input("Escolha: ")

def submenu_fornecedores():
    print("\n--- FORNECEDORES ---")
    print("1 - Cadastrar fornecedor")
    print("2 - Listar fornecedores")
    print("3 - Editar fornecedor")
    print("4 - Deletar fornecedor")
    print("0 - Voltar")
    return input("Escolha: ")

def submenu_formas_pagamento():
    print("\n--- FORMAS DE PAGAMENTO ---")
    print("1 - Cadastrar forma de pagamento")
    print("2 - Listar formas de pagamento")
    print("3 - Editar forma de pagamento")
    print("4 - Deletar forma de pagamento")
    print("0 - Voltar")
    return input("Escolha: ")

def fazer_login():

    global usuario_logado
    print("\n--- LOGIN ---")
    email = input("Email: ")

    if not validar_email(email):
        print("Email inválido!")
        return

    tentativas = 0

    while tentativas < 3:

        senha = input_senha("Senha: ")
        usuario = buscar_usuario_por_email(email)

        if usuario and verificar_senha(senha, usuario["senha"]):
            usuario_logado = usuario
            print(f"Bem-vindo, {usuario_logado['nome']}!")
            return
        
        else:
            tentativas += 1
            restantes = 3 - tentativas
            if restantes > 0:
                print(f"Email ou senha incorretos! {restantes} tentativa(s) restante(s).")
            else:
                print("Número máximo de tentativas atingido! Aguarde 60 segundos...")
                time.sleep(60)
                print("Você pode tentar novamente.")

def main():
    criar_tabelas()

    while True:
        if usuario_logado is None:
            opcao = menu_principal()

            if opcao == "1":
                print("\n--- CADASTRO DE USUÁRIO ---")
                nome  = input("Nome: ")
                email = input("Email: ")

                if not validar_email(email):
                    print("Email inválido!")
                else:
                    if buscar_usuario_por_email(email):
                        print("Email já cadastrado!")
                    else:
                        senha = input_senha("Senha: ")
                        if len(senha) < 6:
                            print("A senha deve ter no mínimo 6 caracteres!")
                        else:
                            confirmar = input_senha("Confirme a senha: ")
                            if senha != confirmar:
                                print("As senhas não coincidem!")
                            else:
                                cadastrar_usuario(nome, email, senha)

            elif opcao == "2":
                fazer_login()

            elif opcao == "0":
                print("Encerrando... Até logo!")
                break

            else:
                print("Opção inválida!")

        else:
            opcao = menu_sistema()

            if opcao == "1":
                while True:
                    sub = submenu_transacoes()

                    if sub == "1":
                        print("\n--- CADASTRAR TRANSAÇÃO ---")
                        categorias = listar_categorias()
                        for c in categorias:
                            print(f"[{c['id']}] {c['nome']} - {c['tipo']}")
                        formas = listar_formas_pagamento()
                        fornecedores = listar_fornecedores()
                        descricao    = input("Descrição: ")
                        valor        = float(input("Valor: "))
                        data         = input("Data (dd/mm/aaaa): ")
                        tipo         = input("Tipo (receita/despesa): ")
                        id_categoria = int(input("ID da categoria: "))
                        id_fornecedor = None
                        id_forma_pagamento = None
                        if fornecedores:
                            print("\nFornecedores:")
                            for f in fornecedores:
                                print(f"[{f['id']}] {f['nome']}")
                            id_fornecedor = int(input("ID do fornecedor (0 para nenhum): ") or 0) or None
                        if formas:
                            print("\nFormas de pagamento:")
                            for f in formas:
                                print(f"[{f['id']}] {f['nome']}")
                            id_forma_pagamento = int(input("ID da forma de pagamento (0 para nenhum): ") or 0) or None
                        cadastrar_transacao(descricao, valor, data, tipo, usuario_logado["id"], id_categoria, id_fornecedor, id_forma_pagamento)

                    elif sub == "2":
                        print("\n--- SUAS TRANSAÇÕES ---")
                        transacoes = listar_transacoes(usuario_logado["id"])
                        if transacoes:
                            for t in transacoes:
                                print(f"[{t['id']}] {t['data']} | {t['descricao']} | R$ {t['valor']:.2f} | {t['tipo']} | {t['categoria']}")
                        else:
                            print("Nenhuma transação cadastrada ainda.")

                    elif sub == "3":
                        print("\n--- BUSCAR TRANSAÇÃO ---")
                        termo = input("Digite o nome para buscar: ")
                        transacoes = buscar_transacao_por_nome(termo, usuario_logado["id"])
                        if transacoes:
                            for t in transacoes:
                                print(f"[{t['id']}] {t['data']} | {t['descricao']} | R$ {t['valor']:.2f} | {t['tipo']} | {t['categoria']}")
                        else:
                            print("Nenhuma transação encontrada.")

                    elif sub == "4":
                        print("\n--- DELETAR TRANSAÇÃO ---")
                        id_transacao = int(input("ID da transação: "))
                        deletar_transacao(id_transacao)

                    elif sub == "0":
                        break

                    else:
                        print("Opção inválida!")

            elif opcao == "2":
                while True:
                    sub = submenu_fornecedores()

                    if sub == "1":
                        print("\n--- CADASTRAR FORNECEDOR ---")
                        nome     = input("Nome: ")
                        cnpj     = input("CNPJ (opcional): ")
                        telefone = input("Telefone (opcional): ")
                        cadastrar_fornecedor(nome, cnpj, telefone)

                    elif sub == "2":
                        print("\n--- FORNECEDORES ---")
                        fornecedores = listar_fornecedores()
                        if fornecedores:
                            for f in fornecedores:
                                print(f"[{f['id']}] {f['nome']} | CNPJ: {f['cnpj']} | Tel: {f['telefone']}")
                        else:
                            print("Nenhum fornecedor cadastrado ainda.")

                    elif sub == "3":
                        print("\n--- EDITAR FORNECEDOR ---")
                        fornecedores = listar_fornecedores()
                        if fornecedores:
                            for f in fornecedores:
                                print(f"[{f['id']}] {f['nome']}")
                            id       = int(input("ID do fornecedor: "))
                            nome     = input("Novo nome: ")
                            cnpj     = input("Novo CNPJ: ")
                            telefone = input("Novo telefone: ")
                            editar_fornecedor(id, nome, cnpj, telefone)
                        else:
                            print("Nenhum fornecedor cadastrado ainda.")

                    elif sub == "4":
                        print("\n--- DELETAR FORNECEDOR ---")
                        fornecedores = listar_fornecedores()
                        if fornecedores:
                            for f in fornecedores:
                                print(f"[{f['id']}] {f['nome']}")
                            id = int(input("ID do fornecedor: "))
                            deletar_fornecedor(id)
                        else:
                            print("Nenhum fornecedor cadastrado ainda.")

                    elif sub == "0":
                        break

                    else:
                        print("Opção inválida!")

            elif opcao == "3":
                while True:
                    sub = submenu_formas_pagamento()

                    if sub == "1":
                        print("\n--- CADASTRAR FORMA DE PAGAMENTO ---")
                        nome = input("Nome: ")
                        cadastrar_forma_pagamento(nome)

                    elif sub == "2":
                        print("\n--- FORMAS DE PAGAMENTO ---")
                        formas = listar_formas_pagamento()
                        if formas:
                            for f in formas:
                                print(f"[{f['id']}] {f['nome']}")
                        else:
                            print("Nenhuma forma de pagamento cadastrada ainda.")

                    elif sub == "3":
                        print("\n--- EDITAR FORMA DE PAGAMENTO ---")
                        formas = listar_formas_pagamento()
                        if formas:
                            for f in formas:
                                print(f"[{f['id']}] {f['nome']}")
                            id   = int(input("ID: "))
                            nome = input("Novo nome: ")
                            editar_forma_pagamento(id, nome)
                        else:
                            print("Nenhuma forma de pagamento cadastrada ainda.")

                    elif sub == "4":
                        print("\n--- DELETAR FORMA DE PAGAMENTO ---")
                        formas = listar_formas_pagamento()
                        if formas:
                            for f in formas:
                                print(f"[{f['id']}] {f['nome']}")
                            id = int(input("ID: "))
                            deletar_forma_pagamento(id)
                        else:
                            print("Nenhuma forma de pagamento cadastrada ainda.")

                    elif sub == "0":
                        break

                    else:
                        print("Opção inválida!")

            elif opcao == "0":
                print("Encerrando... Até logo!")
                break

            else:
                print("Opção inválida!")

main()