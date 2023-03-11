import datetime
import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import (PlanModel, TrainingExerciseModel, TrainingModel,
                     TrainingParametersModel, TrainingResultModel)


class TestRoutinesModels(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser', password='testpassword')

        self.exercise = TrainingExerciseModel.objects.create(
            user=user,
            name="Exercise",
            description='test description'
        )

        self.training = TrainingModel.objects.create(
            user=user,
            name="Training",
        )

        self.trainingparams = TrainingParametersModel.objects.create(
            user=user,
            name=self.training,
            exercise=self.exercise,
            series=5
        )

        self.plan = PlanModel.objects.create(
            user=user,
            name="Plan",
        )
        self.plan.training.add(self.training)

        self.trainingresult = TrainingResultModel.objects.create(
            user=user,
            training=self.trainingparams,
            serie_nr=1,
            weight=20,
            reps=10
        )

    def test_exercise_model(self):
        self.assertEqual(str(self.exercise), "Exercise")

    def test_training_model(self):
        self.assertEqual(str(self.training), "Training")

    def test_training_parameters_model(self):
        self.assertEqual(str(self.trainingparams), "Training-Exercise")

    def test_training_results_model(self):
        self.assertEqual(str(self.trainingresult), "Training-Exercise-1")

    def test_plan_model(self):
        self.assertEqual(str(self.plan), "Plan")


class TestRoutinesViews(APITestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.credentials2 = {
            'username': 'testuser2',
            'password': 'secret'}

        self.user = User.objects.create_user(**self.credentials)
        self.user2 = User.objects.create_user(**self.credentials2)

        self.exercise = TrainingExerciseModel.objects.create(
            user=self.user,
            name="Exercise",
            description='test description'
        )

        self.exercise_next = TrainingExerciseModel.objects.create(
            user=self.user,
            name="Next Exercise",
        )

        self.exercise2 = TrainingExerciseModel.objects.create(
            user=self.user2,
            name="Second Exercise",
        )

        self.training = TrainingModel.objects.create(
            user=self.user,
            name="Training",
        )

        self.training2 = TrainingModel.objects.create(
            user=self.user2,
            name="Another Training",
        )

        self.trainingparams = TrainingParametersModel.objects.create(
            user=self.user,
            name=self.training,
            exercise=self.exercise,
            series=5
        )

        self.plan = PlanModel.objects.create(
            user=self.user,
            name="Plan",
        )
        self.plan.training.add(self.training)

        self.trainingresult = TrainingResultModel.objects.create(
            user=self.user,
            training=self.trainingparams,
            serie_nr=1,
            weight=20,
            reps=10
        )

        self.client.post(reverse('login'), self.credentials)

    def test_exercise_view(self):
        url = reverse('training_exercise-list')

        response = self.client.get(url)
        response_content = json.loads(response.content)['results']

        exercises = TrainingExerciseModel.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_content), exercises.count())

    def test_training_parameters_view(self):
        url = reverse('training_parameters-list')

        data = {
            "name": self.training.pk,
            "exercise": self.exercise_next.pk,
            "series": 4,
            "reps": "8-12",
            "tempo": "31X1",
            "rir": "1-2",
            "rest": 1.5
        }
        response_create = self.client.post(url, data)

        training_params = TrainingParametersModel.objects.filter(
            user=self.user)

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(training_params.count(), 2)

        url_detail = reverse('training_parameters-detail',
                             kwargs={"pk": self.trainingparams.id})

        response_detail = self.client.get(url_detail)

        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail.data["series"], 5)

    def test_creating_training_parameters_with_bad_values(self):
        url = reverse('training_parameters-list')

        data = {
            "name": self.training2.pk,
            "exercise": self.exercise2.pk,
            "series": 4,
            "reps": "8i12",
            "tempo": "31",
            "rir": "1-21",
            "rest": 1.7
        }
        response = self.client.post(url, data)

        training_params = TrainingParametersModel.objects.filter(
            user=self.user)

        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(training_params.count(), 1)
        self.assertEqual(response_data['name'][0], "Error. Improper training")
        self.assertEqual(response_data['exercise'][0],
                         "Error. Improper exercise")
        self.assertEqual(
            response_data['reps'][0], "Reps must be a number or number-number (e.g. 5 or 5-8).")
        self.assertEqual(
            response_data['tempo'][0], "The tempo must be written in this way, e.g. 2011 oraz 31X1")
        self.assertEqual(
            response_data['rir'][0], "RIR must be a number or number-number (e.g. 1 or 1-2).")
        self.assertEqual(
            response_data['rest'][0], "Rest must be a number or a decimal number ending with .5 (e.g. 1.5 or 3)")

    def test_training_view(self):
        url = reverse('r_training-list')

        response = self.client.get(url)
        response_content = json.loads(response.content)['results']

        trainings = TrainingModel.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_content), trainings.count())

    def test_trainings_result_view(self):
        url = reverse('training_result-list')

        response = self.client.get(url)
        response_content = json.loads(response.content)['results']

        trainings = TrainingResultModel.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_content), trainings.count())

        data = {
            "training": self.trainingparams.id,
            "date": datetime.date.today(),
            "serie_nr": 2,
            "weight": 50,
            "reps": 5
        }

        response_create = self.client.post(url, data)

        training_results = TrainingResultModel.objects.filter(
            user=self.user)

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(training_results.count(), 2)

    def test_creating_training_result_with_bad_value(self):
        url = reverse('training_result-list')

        data = {
            "training": self.trainingparams.id,
            "date": datetime.date.today(),
            "serie_nr": 10,
            "weight": 50,
            "reps": 5
        }

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        training_results = TrainingResultModel.objects.filter(
            user=self.user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(training_results.count(), 1)
        self.assertEqual(response_data['serie_nr'][0],
                         "Error. Saved training has fewer series")

    def test_plans_view(self):
        url = reverse('r_plan-list')

        response = self.client.get(url)
        response_content = json.loads(response.content)['results']

        plans = PlanModel.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_content), plans.count())

        data = {
            "name": "Plan Test",
            "training": self.training.id,
        }
        response_create = self.client.post(url, data)

        plans = PlanModel.objects.filter(user=self.user)

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(plans.count(), 2)

    def test_creating_plans_with_bad_value(self):
        url = reverse('r_plan-list')

        data = {
            "name": "Plan Test",
            "training": self.training2.id,
        }

        response = self.client.post(url, data)

        training_results = TrainingResultModel.objects.filter(
            user=self.user)

        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(training_results.count(), 1)
        self.assertEqual(response_data['training'][0],
                         "Error. Improper training")
