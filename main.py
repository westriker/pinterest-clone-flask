import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from forms import FormCriarConta, FormFoto, FormLogin
from models import Foto, Usuario, database

app = Flask(__name__)

app.config["SECRET_KEY"] = "sua_chave_secreta_super_segura"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

database.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "homepage"


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


with app.app_context():
    database.create_all()


@app.route("/", methods=["GET", "POST"])
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for("perfil", usuario=current_user.username))

    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    if request.method == "POST":
        if "btn_login" in request.form and form_login.validate_on_submit():
            usuario = Usuario.query.filter_by(
                email=form_login.email.data
            ).first()
            if usuario and bcrypt.check_password_hash(
                usuario.senha, form_login.senha.data
            ):
                login_user(usuario, remember=form_login.lembrar_dados.data)
                return redirect(url_for("perfil", usuario=usuario.username))

        elif (
            "btn_criarconta" in request.form
            and form_criar_conta.validate_on_submit()
        ):
            senha_cripto = bcrypt.generate_password_hash(
                form_criar_conta.senha.data
            ).decode("utf-8")
            usuario = Usuario(
                username=form_criar_conta.username.data,
                email=form_criar_conta.email.data,
                senha=senha_cripto,
            )
            database.session.add(usuario)
            database.session.commit()

            login_user(usuario, remember=True)
            return redirect(url_for("perfil", usuario=usuario.username))

    return render_template(
        "homepage.html", form_login=form_login, form_criar_conta=form_criar_conta
    )


@app.route("/perfil/<usuario>", methods=["GET", "POST"])
@login_required
def perfil(usuario):
    usuario_objeto = Usuario.query.filter_by(username=usuario).first_or_404()

    # Se for o próprio perfil do usuário logado, permite upload
    if usuario_objeto.id == current_user.id:
        form_foto = FormFoto()

        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)

            # Garante a criação da pasta se não existir
            caminho_pasta = os.path.join(
                app.root_path, app.config["UPLOAD_FOLDER"]
            )
            os.makedirs(caminho_pasta, exist_ok=True)

            # Salva o arquivo no disco
            caminho_completo = os.path.join(caminho_pasta, nome_seguro)
            arquivo.save(caminho_completo)

            # Salva o registro da foto no Banco de Dados
            nova_foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(nova_foto)
            database.session.commit()

            return redirect(url_for("perfil", usuario=current_user.username))

        return render_template(
            "perfil.html", usuario=usuario_objeto, form_foto=form_foto
        )
    else:
        return render_template(
            "perfil.html", usuario=usuario_objeto, form_foto=None
        )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


if __name__ == "__main__":
    app.run(debug=True)