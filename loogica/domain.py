# -*- coding: utf-8 -*-

import re

from coopy.decorators import readonly


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


class PollRepository(object):
    def __init__(self):
        self.polls = []

    def add_poll(self, poll_name, options):
        _id = len(self.polls) + 1
        poll = dict(name=poll_name)
        poll.update(id=_id)

        initialized_options = []
        for op in options:
            initialized_options.append(dict(value=op, votes=0))
        poll.update(options=initialized_options)

        self.polls.append(poll)

    @readonly
    def get_poll(self, _id):
        _id -= 1
        return self.polls[_id]

    def vote(self, poll_id, option):
        poll = self.get_poll(poll_id)
        option -= 1
        poll['options'][option]['votes'] += 1
