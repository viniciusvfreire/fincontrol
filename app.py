from flask import Flask, render_template, request, redirect, url_for, session
from database import criar_tabelas
from usuarios import cadastrar_usuario, buscar_usuario_por_email, verificar_senha
from categorias import cadastrar_categoria, listar_categorias
from transacoes import cadastrar_transacao, listar_transacoes, deletar_transacao

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
    categorias = listar_categorias()
    transacoes = listar_transacoes(session["usuario_id"])
    return render_template("dashboard.html",
                           nome=session["usuario_nome"],
                           categorias=categorias,
                           transacoes=transacoes)

@app.route("/cadastrar-transacao", methods=["POST"])
def nova_transacao():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    descricao    = request.form["descricao"]
    valor        = float(request.form["valor"])
    data         = request.form["data"]
    tipo         = request.form["tipo"]
    id_categoria = int(request.form["id_categoria"])
    cadastrar_transacao(descricao, valor, data, tipo, session["usuario_id"], id_categoria)
    return redirect(url_for("dashboard"))

@app.route("/deletar-transacao/<int:id>")
def deletar(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    deletar_transacao(id)
    return redirect(url_for("dashboard"))

@app.route("/cadastrar-categoria", methods=["POST"])
def nova_categoria():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    nome = request.form["nome"]
    tipo = request.form["tipo"]
    cadastrar_categoria(nome, tipo)
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)