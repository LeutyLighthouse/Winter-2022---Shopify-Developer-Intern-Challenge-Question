def test_addImgPage(app, client):
    res = client.get('/addImg')
    assert res.status_code == 200

def test_addImg(app, client, example_image):
    data = dict(
            file=example_image, 
            image_name="tmp",
            desc="a description",
            c_info="555 555 5555",
            price=27.22,
            is_private=0)
    res = client.post("/uploader",
    content_type='multipart/form-data',
        data=data)
    assert res.status_code == 200 or res.status_code == 302


def test_addImgNoDesc(app, client, example_image):
    data = dict(
            file=example_image, 
            image_name="tmp",
            desc="",
            c_info="555 555 5555",
            price=27.22,
            is_private=0)
    res = client.post("/uploader",
    content_type='multipart/form-data',
        data=data)
    assert res.status_code == 200 or res.status_code == 302

def test_addImgNoName(app, client, captured_templates, example_image):
    data = dict(
            file=example_image, 
            image_name="",
            desc="a description",
            c_info="555 555 5555",
            price=27.22,
            is_private=0)
    res = client.post("/uploader",
    content_type='multipart/form-data',
        data=data)

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "imgUpload.html"
    assert res.status_code == 200 or res.status_code == 302

def test_addImgNoCInfo(app, client, captured_templates, example_image):
    data = dict(
            file=example_image, 
            image_name="tmp",
            desc="a description",
            c_info="",
            price=27.22,
            is_private=0)
    res = client.post("/uploader",
    content_type='multipart/form-data',
        data=data)

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "imgUpload.html"
    assert res.status_code == 200 or res.status_code == 302
    
def test_addImgMultipleEmpty(app, client, captured_templates, example_image):
    data = dict(
            file=example_image, 
            image_name="",
            desc="",
            c_info="",
            price=27.22,
            is_private=0)
    res = client.post("/uploader",
    content_type='multipart/form-data',
        data=data)

    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "imgUpload.html"
    assert res.status_code == 200 or res.status_code == 302
