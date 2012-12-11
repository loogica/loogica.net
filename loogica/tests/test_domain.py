# -*- coding: utf-8 -*-

from loogica.domain import EmailRepository, ValidationError

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
