import pytest
from flask import template_rendered

from server import app as flask_app, User, login_manager
import os
from werkzeug.datastructures import FileStorage

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def captured_templates(app):
    recorded_templates = []
    def record(sender, template, context, **extra):
        recorded_templates.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded_templates
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture
def example_image():
    cwd = os.getcwd()
    filename = cwd + "/tests/test.png"
    fileobj = open(filename, 'rb')
    return FileStorage(stream=fileobj, filename="test.png", content_type="image")