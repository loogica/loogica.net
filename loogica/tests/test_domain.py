# -*- coding: utf-8 -*-

import pytest

from loogica.domain import EmailRepository, ValidationError, \
                           PollRepository

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

def test_poll_repository_init():
    repo = PollRepository()

    assert repo
    assert repo.polls == []

def test_poll_repository_add():
    repo = PollRepository()

    repo.add_poll("Name", [])

    assert repo.polls[0] == dict(id=1,
                                 name="Name",
                                 options=[])

    repo.add_poll("Name2", ["option1"])

    assert repo.polls[1] == dict(id=2,
                                 name="Name2",
                                 options=[{'value': "option1",
                                           'votes': 0}])

    assert len(repo.polls) == 2


def test_poll_repository_get():
    repo = PollRepository()

    repo.add_poll("Name", [])

    assert repo.get_poll(1) == dict(id=1,
                                    name="Name",
                                    options=[])

    repo.add_poll("Name2", ["option1"])

    assert repo.polls[1] == dict(id=2,
                                 name="Name2",
                                 options=[{'value': "option1",
                                           'votes': 0}])

def test_poll_repository_vote():
    repo = PollRepository()

    options = ['op1', 'op2']

    repo.add_poll("Name", options)

    assert repo.get_poll(1) == dict(id=1,
                                    name="Name",
                                    options=[{'value': "op1",
                                              'votes': 0},
                                              {'value': "op2",
                                              'votes': 0}])

    repo.vote(1, 1)

    assert repo.get_poll(1)['options'][0]['votes'] == 1
    assert repo.get_poll(1)['options'][1]['votes'] == 0

    repo.vote(1, 1)

    assert repo.get_poll(1)['options'][0]['votes'] == 2
    assert repo.get_poll(1)['options'][1]['votes'] == 0

    repo.vote(1, 2)

    assert repo.get_poll(1)['options'][0]['votes'] == 2
    assert repo.get_poll(1)['options'][1]['votes'] == 1

    with pytest.raises(Exception):
        repo.vote(1, 3)

