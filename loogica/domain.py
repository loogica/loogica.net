# -*- coding: utf-8 -*-

import re


email_pattern = re.compile('([\w\-\.]+@(\w[\w\-]*\.)+[\w\-]+)')


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

