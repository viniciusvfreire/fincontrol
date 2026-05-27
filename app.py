from flask import Flask, render_template, request, redirect, url_for, session
from database import criar_tabelas
from usuarios import cadastrar_usuario, buscar_usuario_por_email, verificar_senha
from categorias import listar_categorias
from transacoes import cadastrar_transacao, listar_transacoes, deletar_transacao
from fornecedor import cadastrar_fornecedor, listar_fornecedores, editar_fornecedor, deletar_fornecedor
from forma_pagamento import cadastrar_forma_pagamento, listar_formas_pagamento, deletar_forma_pagamento

app = Flask(__name__)
app.secret_key = "fincontrol2026"

criar_tabelas()

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = buscar_usuario_por_email(email)
        if usuario and verificar_senha(senha, usuario["senha"]):
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", erro="Email ou senha incorretos!")
    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome  = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        cadastrar_usuario(nome, email, senha)
        return redirect(url_for("login"))
    return render_template("cadastro.html")

@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    categorias   = listar_categorias()
    transacoes   = listar_transacoes(session["usuario_id"])
    fornecedores = listar_fornecedores()
    formas       = listar_formas_pagamento()
    return render_template("dashboard.html",
                           nome=session["usuario_nome"],
                           categorias=categorias,
                           transacoes=transacoes,
                           fornecedores=fornecedores,
                           formas=formas)

@app.route("/cadastrar-transacao", methods=["POST"])
def nova_transacao():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    descricao          = request.form["descricao"]
    valor              = float(request.form["valor"])
    data               = request.form["data"]
    tipo               = request.form["tipo"]
    id_categoria       = int(request.form["id_categoria"])
    id_fornecedor      = request.form.get("id_fornecedor") or None
    id_forma_pagamento = request.form.get("id_forma_pagamento") or None
    if id_fornecedor:
        id_fornecedor = int(id_fornecedor)
    if id_forma_pagamento:
        id_forma_pagamento = int(id_forma_pagamento)
    cadastrar_transacao(descricao, valor, data, tipo, session["usuario_id"], id_categoria, id_fornecedor, id_forma_pagamento)
    return redirect(url_for("dashboard"))

@app.route("/deletar-transacao/<int:id>")
def deletar(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    deletar_transacao(id)
    return redirect(url_for("dashboard"))

@app.route("/cadastrar-fornecedor", methods=["POST"])
def novo_fornecedor():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    nome     = request.form["nome"]
    cnpj     = request.form.get("cnpj", "")
    telefone = request.form.get("telefone", "")
    cadastrar_fornecedor(nome, cnpj, telefone)
    return redirect(url_for("dashboard"))

@app.route("/deletar-fornecedor/<int:id>")
def remover_fornecedor(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    deletar_fornecedor(id)
    return redirect(url_for("dashboard"))

@app.route("/cadastrar-forma-pagamento", methods=["POST"])
def nova_forma_pagamento():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    nome = request.form["nome"]
    cadastrar_forma_pagamento(nome)
    return redirect(url_for("dashboard"))

@app.route("/deletar-forma-pagamento/<int:id>")
def remover_forma_pagamento(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    deletar_forma_pagamento(id)
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)