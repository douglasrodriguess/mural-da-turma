import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# Lê o .env (que NÃO vai pro Git)
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")  # assina a sessão do login

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Faça login para comentar no mural."


# ---------- MODELS ----------
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)

    # um usuário tem vários comentários (relacionamento 1:N)
    comentarios = db.relationship("Comentario", backref="autor", lazy=True)

    def definir_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)  # nunca salvar a senha pura

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # chave estrangeira: cada comentário pertence a um usuário
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)


@login_manager.user_loader
def carregar_usuario(user_id):
    return db.session.get(Usuario, int(user_id))


# Cria as tabelas que ainda não existem (não apaga nem altera as que já existem)
with app.app_context():
    db.create_all()


# ---------- CONTROLLERS ----------
@app.route("/")
def index():
    comentarios = Comentario.query.order_by(Comentario.criado_em.desc()).all()
    return render_template("index.html", comentarios=comentarios)


@app.route("/comentar", methods=["POST"])
@login_required
def comentar():
    texto = request.form["texto"].strip()
    if texto:
        db.session.add(Comentario(texto=texto, autor=current_user))
        db.session.commit()
        flash("Comentário publicado!")
    return redirect(url_for("index"))


@app.route("/comentario/<int:id>/excluir", methods=["POST"])
@login_required
def excluir(id):
    comentario = db.get_or_404(Comentario, id)
    if comentario.autor != current_user:
        abort(403)  # só o autor pode excluir o próprio comentário
    db.session.delete(comentario)
    db.session.commit()
    flash("Comentário excluído.")
    return redirect(url_for("index"))


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        if Usuario.query.filter_by(email=email).first():
            flash("Este e-mail já está cadastrado.")
            return redirect(url_for("cadastro"))

        usuario = Usuario(nome=request.form["nome"], email=email)
        usuario.definir_senha(request.form["senha"])
        db.session.add(usuario)
        db.session.commit()

        login_user(usuario)
        flash(f"Bem-vindo(a), {usuario.nome}!")
        return redirect(url_for("index"))

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.verificar_senha(request.form["senha"]):
            login_user(usuario)
            return redirect(url_for("index"))

        flash("E-mail ou senha inválidos.")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
