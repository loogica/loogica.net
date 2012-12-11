# -*- coding: utf-8 -*-

from wtforms import Form, TextField, validators


MESSAGE1 = u"O nome é necessário"
MESSAGE2 = u"Tamanho inferior a 3"
MESSAGE3 = u'Email sem tamanho mínimo'
MESSAGE4 = u'Email inválido'


class UserForm(Form):
    name = TextField('Nome',
                     [validators.Required(message=MESSAGE1),
                      validators.Length(min=3, max=100,
                                        message=MESSAGE2)],
                     default="")
    email = TextField('Email',
                      [validators.Length(min=5, message=MESSAGE3),
                       validators.Email(message=MESSAGE4)], default="")
