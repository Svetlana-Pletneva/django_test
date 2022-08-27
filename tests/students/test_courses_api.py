from rest_framework.test import APIClient
import pytest
from django.contrib.auth.models import User
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def user():
    return User.objects.create_user('admin')


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


# проверка получения 1го курса (retrieve-логика)
@pytest.mark.django_db
def test_get_first_course(client, courses_factory):
    courses = courses_factory(_quantity=20)
    index = 1
    course = courses[index].id
    response = client.get(f'/courses/{course}/')
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == courses[index].name


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_courses_list(client, courses_factory):
    courses = courses_factory(_quantity=20)
    response = client.get('/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(courses)


# тест успешного создания курса
@pytest.mark.django_db
def test_filter_id(client):
    response = client.post('/courses/', data={'name': 'Python'})
    assert response.status_code == 201


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_course_id(client, courses_factory):
    courses = courses_factory(_quantity=20)
    index = 17
    course = courses[index].id
    base_url = '/courses/'
    response = client.get(base_url, data={'id': course})
    assert response.status_code == 200


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_course_name(client, courses_factory):
    courses = courses_factory(_quantity=5)
    index = 2
    course = courses[index].name
    base_url = '/courses/'
    response = client.get(base_url, data={'name': course})
    assert response.status_code == 200
    assert response is not []


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, courses_factory):
    courses = courses_factory(_quantity=20)
    index = 6
    course = courses[index].id
    base_url = f'/courses/{course}/'
    response = client.patch(base_url, data={'name': 'Hello'})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Hello'


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    courses = courses_factory(_quantity=20)
    index = 12
    course = courses[index].id
    response = client.delete(f'/courses/{course}/')
    assert response.status_code == 204