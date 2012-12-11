# -*- coding: utf-8 -*-

from coopy.base import init_persistent_system
from flask import Flask, jsonify, render_template, request, flash

from loogica.domain import EmailRepository, ValidationError
from loogica.forms import UserForm

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
    app.secret_key = open('prod_key.key').read()
    app.run(debug=True)
