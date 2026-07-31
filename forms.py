from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from models import Usuario
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    lembrar_dados = BooleanField("Lembrar dados de acesso")
    botao_confirmacao = SubmitField("Fazer Login")


class FormCriarConta(FlaskForm):
    username = StringField("Nome de Usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    confirmacao_senha = PasswordField(
        "Confirme a Senha", validators=[DataRequired(), EqualTo("senha")]
    )
    botao_confirmacao = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado.")


# Formulário para Envio de Fotos
class FormFoto(FlaskForm):
    foto = FileField(
        "Foto",
        validators=[
            DataRequired(),
            FileAllowed(["jpg", "png", "jpeg", "webp"], "Apenas imagens!"),
        ],
    )
    botao_confirmacao = SubmitField("Enviar Foto")