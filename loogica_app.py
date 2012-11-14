# -*- coding: utf-8 -*-

import re

from coopy.base import init_persistent_system
from flask import Flask, jsonify, render_template, request, flash
from wtforms import Form, TextField, validators

email_pattern = re.compile('([\w\-\.]+@(\w[\w\-]*\.)+[\w\-]+)')

class UserForm(Form):
    name = TextField('Nome',
                     [validators.Required(message=u"O nome é necessário"),
                      validators.Length(min=3, max=100,
                                        message="Tamanho inferior a 3")
                     ],
                     default="",
                    )
    email = TextField('Email',
                      [
                       validators.Length(min=5, message=u'Email sem tamanho mínimo'),
                       validators.Email(message=u'Email inválido')
                      ],
                      default="")

class ValidationError(Exception):
    def __init__(self, data):
        for k, v in data.items():
            if isinstance(v, unicode):
                data[k] = v.encode('utf-8')
        self.data = data

    def __str__(self):
        return "{field} - {message}".format(**self.data)

    def __unicode__(self):
        return "{field} - {message}".format(**self.data)

class EmailRepository(object):
    def __init__(self):
        self.users = {}

    def add_user(self, name, email):
        email = email.strip()
        if not len(name.strip()) > 0:
            raise ValidationError({'field': 'name',
                                   'message': u'Nome inválido'})
        if not self.valid_email(email):
            raise ValidationError({'field': 'email',
                                'message': u'Email inválido'})
        self.users[email] = dict(name=name.strip())

    def valid_email(self, email):
        return email_pattern.search(email) >= 0

def test_email_repository_init():
    repo = EmailRepository()

    assert repo
    assert repo.users == {}

def test_email_repository_valid_email():
    repo = EmailRepository()

    assert repo.valid_email("felipecruz@loogica.net")

def test_email_repository_invalid_email():
    repo = EmailRepository()

    assert not repo.valid_email("felipecruzloogica.net")
    assert not repo.valid_email("error@loogica.")

def test_email_repository_add_user_success():
    repo = EmailRepository()

    repo.add_user("Felipe", "felipecruz@loogica.net")

    assert "felipecruz@loogica.net" in repo.users
    assert dict(name="Felipe") == repo.users['felipecruz@loogica.net']
    assert dict(name="Felipe") == repo.users.values()[0]

def test_email_repository_add_user_error():
    repo = EmailRepository()

    try:
        repo.add_user("Felipe", "felipecruz@loogica.")
        assert False
    except:
        assert True

app = Flask(__name__)
repository = init_persistent_system(EmailRepository())

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/participar", methods=['GET', 'POST'])
def create_user():
    if request.method == "GET":
        form = UserForm()
        return render_template('quero-participar.html', form=form)

    form = UserForm(request.form)
    errors = None

    if form.validate():
        try:
            repository.add_user(form.name.data, form.email.data)
            flash('Seu usuário foi cadastrado com sucesso')
            return render_template('quero-participar-cadastrado.html')
        except ValidationError as ve:
            errors = ve.data

    return render_template('quero-participar.html', form=form,
                                                    errors=errors)
@app.route("/usuarios")
def users_list():
    return jsonify(repository.users)

if __name__ == "__main__":
    app.secret_key = '\xfcUQ\xef\x9f\x8e\x83\x10\xdc\xb4R\rk\x9ao\xfcn\xf3\xf8\xd3\x0e\xfb;('
    app.run(debug=True)
