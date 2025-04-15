
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest


import pytest
from ads.models import Ad, Category, ExchangeProposal
from django.contrib.auth.models import User


import io

from PIL import Image

from ads.models import Category, ExchangeProposal


@pytest.fixture
def generate_test_image():
    file = io.BytesIO()
    image = Image.new('RGB', (100, 100), color='red')
    image.save(file, 'jpeg')
    file.name = 'test.jpg'
    file.seek(0)
    return file


@pytest.fixture
def uploaded_file(generate_test_image):
    image_file = generate_test_image
    return SimpleUploadedFile(
        name='test.jpg', content=image_file.read(), content_type='image/jpeg')


@pytest.fixture
def category():
    return Category.objects.create(name="Electronics")
