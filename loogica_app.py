# -*- coding: utf-8 -*-

from coopy.base import init_persistent_system
from flask import Flask, jsonify, render_template, request, flash

from loogica.domain import EmailRepository, ValidationError, PollRepository
from loogica.forms import UserForm

app = Flask(__name__)
user_repo = init_persistent_system(EmailRepository(), basedir="emailrepository")
poll_repo = init_persistent_system(PollRepository())

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
            user_repo.add_user(form.name.data, form.email.data)
            flash('Seu usuário foi cadastrado com sucesso')
            return render_template('quero-participar-cadastrado.html')
        except ValidationError as ve:
            errors = ve.data

    return render_template('quero-participar.html', form=form,
                                                    errors=errors)
@app.route("/usuarios")
def users_list():
    return jsonify(user_repo.users)

@app.route("/polls")
def polls():
    return jsonify(dict(polls=poll_repo.polls))

@app.route("/poll/<int:poll_id>")
def poll(poll_id):
    return jsonify(poll_repo.get_poll(poll_id))

@app.route("/poll/vote/<int:poll_id>/<int:option_id>")
def vote(poll_id, option_id):
    poll_repo.vote(poll_id, option_id)
    return jsonify(poll_repo.get_poll(poll_id))

if __name__ == "__main__":
    app.secret_key = open('prod_key.key').read()
    app.run(debug=True)
