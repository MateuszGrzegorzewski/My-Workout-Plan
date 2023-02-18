from django.contrib.auth.models import User
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Exercise, Muscle


class TestMuclewikiModels(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testuser', password='testpassword')

        cls.muscle = Muscle.objects.create(
            name="Muscle Test"
        )

        cls.exercise = Exercise.objects.create(
            user=user,
            name="Exercise Test",
            technique="Technique of Exercise"
        )
        cls.exercise.muscle.add(cls.muscle)

    def test_muscle_model(self):
        self.assertEqual(str(self.muscle), 'Muscle Test')

    def test_exercise_model(self):
        self.assertEqual(str(self.exercise), 'Exercise Test')


class TestMusclewikiViews(APITestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}

        self.credentials_admin = {
            'username': 'testadmin',
            'password': 'secretadmin'}

        self.user = User.objects.create_user(**self.credentials)
        self.admin = User.objects.create_superuser(**self.credentials_admin)

        self.muscle = Muscle.objects.create(
            name="Muscle Test"
        )

        self.exercise = Exercise.objects.create(
            user=self.admin,
            name="Exercise Test",
            technique="Technique of Exercise"
        )
        self.exercise.muscle.add(self.muscle.id)

        self.exercise_user = Exercise.objects.create(
            user=self.user,
            name="Exercise Test by User",
            technique="Technique of Exercise"
        )
        self.exercise.muscle.add(self.muscle.id)

    def test_CRUD_Muscle_View_Set(self):
        self.client.post('/login/', self.credentials_admin)

        url_list = reverse('musclewiki:muscles-list')

        response_list = self.client.get(url_list)

        qs_list = Muscle.objects.all()

        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(qs_list.count(), 1)

        data = {
            "name": 'Muscle Test2'
        }
        response_create = self.client.post(url_list, data)

        qs_create = Muscle.objects.all()

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(qs_create.count(), 2)

        url_detail = reverse('musclewiki:muscles-detail',
                             kwargs={"pk": self.muscle.id})

        response_detail = self.client.get(url_detail)

        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail.data["muscle"]['name'], 'Muscle Test')

        data_to_update = {
            "name": 'Muscle Test Update'
        }
        response_update = self.client.patch(url_detail, data_to_update)

        qs_update = Muscle.objects.get(id=self.muscle.id)

        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(qs_update.name, 'Muscle Test Update')

        response_delete = self.client.delete(url_detail)

        qs_delete = Muscle.objects.all()

        self.assertEqual(response_delete.status_code, 204,
                         "Delete the element from database.")
        self.assertEqual(qs_delete.count(), 1)

    def test_CRUD_Muscle_View_Set_with_random_user(self):
        self.client.post('/login/', self.credentials)

        url_list = reverse('musclewiki:muscles-list')

        response_list = self.client.get(url_list)

        qs_list = Muscle.objects.all()

        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(qs_list.count(), 1)

        data = {
            "name": 'Muscle Test2'
        }
        response_create = self.client.post(url_list, data)

        qs_create = Muscle.objects.all()

        self.assertEqual(response_create.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(qs_create.count(), 1)

        url_detail = reverse('musclewiki:muscles-detail',
                             kwargs={"pk": self.muscle.id})

        response_detail = self.client.get(url_detail)

        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail.data["muscle"]['name'], 'Muscle Test')

        data_to_update = {
            "name": 'Muscle Test Update'
        }
        response_update = self.client.patch(url_detail, data_to_update)

        qs_update = Muscle.objects.get(id=self.muscle.id)

        self.assertEqual(response_update.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(qs_update.name, 'Muscle Test Update')

        response_delete = self.client.delete(url_detail)

        qs_delete = Muscle.objects.all()

        self.assertEqual(response_delete.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(qs_delete.count(), 1)

    def test_CRUD_Muscle_View_Set_without_authentication(self):
        url_list = reverse('musclewiki:muscles-list')

        response_list = self.client.get(url_list)

        qs_list = Muscle.objects.all()

        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(qs_list.count(), 1)

        data = {
            "name": 'Muscle Test2'
        }
        response_create = self.client.post(url_list, data)

        qs_create = Muscle.objects.all()

        self.assertEqual(response_create.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(qs_create.count(), 1)

        url_detail = reverse('musclewiki:muscles-detail',
                             kwargs={"pk": self.muscle.id})

        response_detail = self.client.get(url_detail)

        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail.data["muscle"]['name'], 'Muscle Test')

        data_to_update = {
            "name": 'Muscle Test Update'
        }
        response_update = self.client.patch(url_detail, data_to_update)

        qs_update = Muscle.objects.get(id=self.muscle.id)

        self.assertEqual(response_update.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(qs_update.name, 'Muscle Test Update')

        response_delete = self.client.delete(url_detail)

        qs_delete = Muscle.objects.all()

        self.assertEqual(response_delete.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(qs_delete.count(), 1)

    def test_Exercise_View_Set_CREATE(self):
        self.client.post('/login/', self.credentials_admin)

        url = reverse('exercise-create')

        data = {
            "user": self.admin,
            "name": 'Muscle Test by Admin',
            "muscle": self.muscle.id,
            'technique': "Technique of exercise"
        }
        response_create = self.client.post(url, data)

        qs = Exercise.objects.all()

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(qs.count(), 3)

    def test_Exercise_View_Set_CREATE_without_authentication(self):
        url = reverse('exercise-create')

        data = {
            "user": self.admin,
            "name": 'Exercise Test by Admin',
            "muscle": self.muscle.id,
            'technique': "Technique of exercise"
        }
        response_create = self.client.post(url, data)

        qs = Exercise.objects.all()

        self.assertEqual(response_create.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(qs.count(), 2)

    def test_Exercise_View_Set_DETAIL_UPDATE_DELETE_with_admin(self):
        self.client.post('/login/', self.credentials_admin)

        url = reverse('exercise-detail-update-delete',
                      kwargs={"pk": self.exercise.id})

        response_detail = self.client.get(url)

        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail.data["name"], 'Exercise Test')

        data = {
            "user": self.admin,
            "name": 'Exercise Test by Admin',
            "muscle": self.muscle.id,
            'technique': "Technique of exercise"
        }
        response_update = self.client.patch(url, data)

        qs_update = Exercise.objects.get(id=self.exercise.id)

        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(qs_update.name, 'Exercise Test by Admin')

        response_delete = self.client.delete(url)

        qs_delete = Exercise.objects.all()

        self.assertEqual(response_delete.status_code, 204,
                         "Delete the element from database.")
        self.assertEqual(qs_delete.count(), 1)

    def test_Exercise_View_Set_DETAIL_UPDATE_DELETE_with_no_authentication(self):
        url = reverse('exercise-detail-update-delete',
                      kwargs={"pk": self.exercise.id})

        response_detail = self.client.get(url)

        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail.data["name"], 'Exercise Test')

        data = {
            "user": self.admin,
            "name": 'Exercise Test Update',
            "muscle": self.muscle.id,
            'technique': "Technique of exercise"
        }
        response_update = self.client.patch(url, data)

        qs_update = Exercise.objects.get(id=self.exercise.id)

        self.assertEqual(response_update.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(qs_update.name, 'Exercise Test Update')

        response_delete = self.client.delete(url)

        qs_delete = Exercise.objects.all()

        self.assertEqual(response_delete.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(qs_delete.count(), 2)

    def test_Exercise_View_Set_DETAIL_UPDATE_DELETE_permissions_with_random_user(self):
        self.client.post('/login/', self.credentials)

        url = reverse('exercise-detail-update-delete',
                      kwargs={"pk": self.exercise.id})

        response_detail = self.client.get(url)

        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail.data["name"], 'Exercise Test')

        data = {
            "user": self.admin,
            "name": 'Exercise Test Update',
            "muscle": self.muscle.id,
            'technique': "Technique of exercise"
        }
        response_update = self.client.patch(url, data)

        qs_update = Exercise.objects.get(id=self.exercise.id)

        self.assertEqual(response_update.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(qs_update.name, 'Exercise Test Update')

        response_delete = self.client.delete(url)

        qs_delete = Exercise.objects.all()

        self.assertEqual(response_delete.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(qs_delete.count(), 2)

    def test_Exercise_View_Set_DETAIL_UPDATE_DELETE_permissions_with_admin(self):
        self.client.post('/login/', self.credentials_admin)

        url = reverse('exercise-detail-update-delete',
                      kwargs={"pk": self.exercise_user.id})

        response_detail = self.client.get(url)

        self.assertEqual(response_detail.status_code,
                         status.HTTP_403_FORBIDDEN)

        data = {
            "user": self.admin,
            "name": 'Exercise Test by Admin',
            "muscle": self.muscle.id,
            'technique': "Technique of exercise"
        }
        response_update = self.client.patch(url, data)

        qs_update = Exercise.objects.get(id=self.exercise.id)

        self.assertEqual(response_update.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(qs_update.name, 'Exercise Test by Admin')

        response_delete = self.client.delete(url)

        qs_delete = Exercise.objects.all()

        self.assertEqual(response_delete.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(qs_delete.count(), 2)


class TestMusclewikiViewsValidation(TransactionTestCase):
    def setUp(self):
        self.credentials_admin = {
            'username': 'testadmin',
            'password': 'secretadmin'}

        self.admin = User.objects.create_superuser(**self.credentials_admin)

        self.muscle = Muscle.objects.create(
            name="Muscle Test"
        )

        self.exercise = Exercise.objects.create(
            user=self.admin,
            name="Exercise Test",
            technique="Technique of Exercise"
        )
        self.exercise.muscle.add(self.muscle.id)

    def test_Muscle_View_Set_with_wrong_values_in_endpoint(self):
        self.client.post('/login/', self.credentials_admin)

        url = reverse('musclewiki:muscles-detail',
                      kwargs={"pk": 999})

        response_detail = self.client.get(url)

        self.assertEqual(response_detail.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_Exercise_View_Set_CREATE_unique_of_name(self):
        self.client.post('/login/', self.credentials_admin)

        url = reverse('exercise-create')

        data = {
            "user": self.admin,
            "name": 'Exercise Test',
            "muscle": self.muscle.id,
            'technique': "Technique of exercise"
        }
        response = self.client.post(url, data)

        qs = Exercise.objects.all()

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(qs.count(), 1)

    def test_Exercise_View_Set_UPDATE_unique_of_name(self):
        self.client.post('/login/', self.credentials_admin)

        url = reverse('exercise-detail-update-delete',
                      kwargs={"pk": self.exercise.id})

        Exercise.objects.create(
            user=self.admin,
            name="Exercise Test New",
            technique="Technique of Exercise"
        )

        data = {
            "user": self.admin,
            "name": 'Exercise Test New',
            "muscle": self.muscle.id,
            'technique': "Technique of exercise"
        }
        self.client.patch(url, data)

        qs_update = Exercise.objects.get(id=self.exercise.id)

        self.assertNotEqual(qs_update.name, 'Exercise Test New')
