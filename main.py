from database import criar_tabelas
from usuarios import cadastrar_usuario, buscar_usuario_por_email
from categorias import cadastrar_categoria, listar_categorias
from transacoes import cadastrar_transacao, listar_transacoes, deletar_transacao, editar_transacao

usuario_logado = None


def menu_principal():
    while True:
        print("\n=== Controle de Gastos ===")
        print("1 - Cadastrar Usuário")
        print("2 - Fazer login")
        print("0 - Sair")
        return(input("Escolha uma opção: "))
    
def menu_sistema():
    print(f"\n OLÁ, {usuario_logado['nome'].upper()}!")
    print("1 - Cadastrar categoria")
    print("2 - Listar categorias")
    print("3 - Cadastrar transação")
    print("4 - Listar transações")  
    print("5 - Deletar transações")
    print("6 - Sair")
    return(input("Escolha uma opção: "))

def fazer_login():
    global usuario_logado

    print("\nLogin ")    
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")

    usuario = buscar_usuario_por_email(email)

    if usuario and usuario['senha'] == senha:
        usuario_logado = usuario
        print(f"Bem-vindo, {usuario_logado['nome']}!")
    else:
        print("Email ou senha incorretos. Tente novamente.")

def main():
    criar_tabelas()

    while True:

        if usuario_logado is None: 
            opcao = menu_principal()

            
            if opcao == "1":
                print("\nCadastro de usuário")
                nome = input("Digite seu nome: ")
                email = input("Digite seu email: ")
                senha = input("Digite sua senha: ")
                cadastrar_usuario(nome, email, senha)

            elif opcao == "2":  
                fazer_login()

            elif opcao == "0":
                print("Saindo do programa. Até mais!")
                break

            else:
                print("Opção inválida.")    

        else: 
            opcao = menu_sistema()

            if opcao == "1":
                print("\nCadastro de categoria")
                nome = input("Digite o nome da categoria: ")
                tipo = input("Digite o tipo (receita ou despesa): ")
                cadastrar_categoria(nome, tipo)

            elif opcao == "2":
                print("\n--- CATEGORIAS CADASTRADAS ---")

                categorias = listar_categorias()

                if categorias:
                    for c in categorias:
                        print(f"[{c['id']}] {c['nome']} - {c['tipo']}")

                else:
                    print("Nenhuma categoria cadastrada ainda.")
            
            elif opcao == "3":
                print("\n--- CADASTRAR TRANSAÇÃO ---")
                categorias = listar_categorias()    

                if not categorias:
                    print("Cadastre uma categoria primeiro!") 
