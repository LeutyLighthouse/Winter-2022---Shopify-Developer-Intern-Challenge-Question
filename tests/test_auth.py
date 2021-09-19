from flask import url_for, request

def test_loginPageLoads(app, client, captured_templates):
    res = client.get("/login")

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "login.html"
    assert res.status_code == 200 or res.status_code == 302

def test_signupPageLoads(app, client, captured_templates):
    res = client.get("/signup")

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "signup.html"
    assert res.status_code == 200 or res.status_code == 302

def test_redirectRegisterNoLogin(app, client):
    with client:
        res = client.get("/register", follow_redirects=True)
        assert request.path == url_for('login')

def test_redirectLoggingInNoLogin(app, client):
    with client:
        res = client.get("/loggingIn", follow_redirects=True)
        assert request.path == url_for('login')

def test_registerAndLogin(app, client):
    with client:
        data = dict(
                username="user", 
                password="password")
        res = client.post("/register",
                content_type='multipart/form-data',
                data=data, follow_redirects=True)

        data = dict(
                username="user", 
                password="password")
        res = client.post("/loggingIn",
                content_type='multipart/form-data',
                data=data, follow_redirects=True)

        assert request.path == url_for('home_page')

def test_registerAndLogin2(app, client, captured_templates):
    with client:
        data = dict(
                username="a", 
                password="a")
        res = client.post("/register",
                content_type='multipart/form-data',
                data=data, follow_redirects=True)

        data = dict(
                username="a", 
                password="a")
        res = client.post("/loggingIn",
                content_type='multipart/form-data',
                data=data, follow_redirects=True)

        assert request.path == url_for('home_page')
        res = client.get("/")
        template, context = captured_templates[2]
        assert template.name == "index.html"


def test_registerEmptyName(app, client, captured_templates):
    with client:
        data = dict(
                username="", 
                password="aaa")
        res = client.post("/register",
                content_type='multipart/form-data',
                data=data, follow_redirects=True)

        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        assert template.name == "signup.html"

def test_registerEmptyPassword(app, client, captured_templates):
    with client:
        data = dict(
                username="aaa", 
                password="")
        res = client.post("/register",
                content_type='multipart/form-data',
                data=data, follow_redirects=True)

        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        assert template.name == "signup.html"


def test_registerSameUser(app, client, captured_templates):
    with client:
        data = dict(
                username="aaa", 
                password="aaa")
        res = client.post("/register",
                content_type='multipart/form-data',
                data=data, follow_redirects=True)

        res = client.post("/register",
                content_type='multipart/form-data',
                data=data, follow_redirects=True)

        template, context = captured_templates[1]
        assert template.name == "signup.html"
