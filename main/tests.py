from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Plan, PlanName, TrainingMain, TrainingName, TrainingResult


class TestMainModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="testuser", password="passw123")

        cls.training_name = TrainingName.objects.create(
            user=user,
            name="Training Test")

        cls.training_main = TrainingMain.objects.create(
            user=user,
            name_id=cls.training_name.pk,
            exercise="Exercise Test")

        cls.training_result = TrainingResult.objects.create(
            user=user,
            name_id=cls.training_name.pk,
            exercise_id=cls.training_main.pk,
            series="Serie Test")

        cls.plan_name = PlanName.objects.create(
            user=user,
            name="Plan Test")

    def test_trainingname_model_str(self):
        self.assertEqual(str(self.training_name), 'Training Test')

    def test_trainingmain_model_str(self):
        self.assertEqual(str(self.training_main), 'Exercise Test')

    def test_trainingresult_model_str(self):
        self.assertEqual(str(self.training_result), 'Serie Test')

    def test_planname_model_str(self):
        self.assertEqual(str(self.plan_name), 'Plan Test')


class TestAccount(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}

        self.credentials_invalid = {
            'username': 'testuser2',
            'password': 'secret1'}

        self.credentials_register = {
            'username': 'usertest',
            'password1': 'Mypassword123',
            'password2': 'Mypassword123'}

        self.credentials_register_invalid = {
            'username': 'usertest1',
            'password1': 'Mypassword1',
            'password2': 'Mypassword123'}

        User.objects.create_user(**self.credentials)

    def test_login(self):
        response_to_test_template = self.client.get('/login/')
        response = self.client.post('/login/', self.credentials, follow=True)

        self.assertTemplateUsed(response_to_test_template,
                                'main/login_register.html')
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/')

    def test_login_invalid(self):
        response_invalid = self.client.post(
            '/login/', self.credentials_invalid, follow=True)

        self.assertFalse(response_invalid.context['user'].is_authenticated)

    def test_login_user_which_is_authenticated(self):
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.post('/login/', self.credentials, follow=True)

        self.assertRedirects(response, '/')

    def test_logout(self):
        response_login = self.client.post(
            '/login/', self.credentials, follow=True)

        self.assertTrue(response_login.context['user'].is_authenticated)

        response = self.client.post('/logout/', follow=True)

        self.assertFalse(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/')

    def test_register(self):
        response_to_test_template = self.client.get('/register/')
        response = self.client.post(
            '/register/', follow=True, data=self.credentials_register)

        self.assertTemplateUsed(
            response_to_test_template, template_name='main/login_register.html')

        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 2)

    def test_register_invalid(self):
        response = self.client.post(
            '/register/', follow=True, data=self.credentials_register_invalid)

        self.assertContains(
            response, "Unsuccessful registration. Invalid information.")


class TestMainViews(TestCase):
    @classmethod
    def setUp(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'}

        cls.credentials2 = {
            'username': 'testuser2',
            'password': 'secret'}

        cls.user = User.objects.create_user(**cls.credentials)
        cls.user2 = User.objects.create_user(**cls.credentials2)

        cls.training_name = TrainingName.objects.create(
            user=cls.user,
            name="Training Test"
        )

        cls.training_main = TrainingMain.objects.create(
            user=cls.user,
            name_id=cls.training_name.pk,
            exercise="Exercise Test")

        cls.training_result = TrainingResult.objects.create(
            user=cls.user,
            name_id=cls.training_name.pk,
            exercise_id=cls.training_main.pk,
            series="Serie Test")

        cls.plan_name = PlanName.objects.create(
            user=cls.user,
            name="Plan Test"
        )

        cls.plan = Plan.objects.create(
            user=cls.user,
            name_id=cls.plan_name.pk,
            training_id=cls.training_name.pk
        )

    def test_home_view_GET(self):
        response = self.client.get('')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_plan_view_GET(self):
        self.client.post('/login/', self.credentials, follow=True)

        response = self.client.get('/plan/')

        qs_plan_name = PlanName.objects.filter(user=self.user)

        self.assertEqual(qs_plan_name.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/plan.html')

    def test_plan_view_POST(self):
        self.client.post('/login/', self.credentials, follow=True)

        response = self.client.post('/create-plan/', follow=True, data={
            'user': self.user,
            'name': 'Plan Test 2'
        })
        response_to_test_template = self.client.get('/create-plan/')

        qs = PlanName.objects.last()

        self.assertTemplateUsed(response_to_test_template,
                                'main/plan_main_form.html')
        self.assertRedirects(response, "/plan/")
        self.assertEqual(qs.name, 'Plan Test 2')

    def test_plan_view_POST_with_incorrect_values(self):
        self.client.post('/login/', self.credentials, follow=True)

        response = self.client.post('/create-plan/', follow=True, data={
            'user': self.user,
            'name': 'Plan Test'
        })

        self.assertContains(response, 'Error occured during')

    def test_plan_view_UPDATE(self):
        self.client.post('/login/', self.credentials, follow=True)

        response = self.client.post(reverse('update-plan', args=(self.plan_name.id,)), follow=True, data={
            'name': 'Plan Test 1'
        })
        response_to_test_template = self.client.post(
            reverse('update-plan', args=(self.plan_name.id,)))

        qs = PlanName.objects.get(pk=self.plan_name.id)

        self.assertTemplateUsed(
            response_to_test_template, 'main/create_form.html')
        self.assertRedirects(response, "/plan/")
        self.assertEqual(qs.name, 'Plan Test 1')

    def test_nonexistent_plan_view_UPDATE(self):
        self.client.post('/login/', self.credentials, follow=True)

        response = self.client.post(reverse('update-plan', args=(999,)), follow=True, data={
            'name': 'Plan Test 1'
        })

        self.assertTemplateUsed(response, 'errors/404.html')

    def test_plan_view_UPDATE_with_incorrect_values(self):
        self.client.post('/login/', self.credentials, follow=True)

        PlanName.objects.create(
            user=self.user,
            name="Plan Test New"
        )

        response = self.client.post(reverse('update-plan', args=(self.plan_name.id,)), follow=True, data={
            'name': 'Plan Test New'
        })

        self.assertContains(response, "Error occured during")

    def test_plan_view_UPDATE_another_user(self):
        self.client.post('/login/', self.credentials2, follow=True)

        response = self.client.post(reverse('update-plan', args=[self.plan_name.id]), data={
            'name': 'Plan Test I'
        })

        qs = PlanName.objects.get(pk=self.plan_name.id)

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(qs.name, 'Plan Test I')

    def test_plan_view_DELETE(self):
        self.client.post('/login/', self.credentials, follow=True)

        response_to_test_template = self.client.get(
            reverse('delete-plan', args=[self.plan_name.id]))
        response = self.client.post(
            reverse('delete-plan', args=[self.plan_name.id]), follow=True)

        qs = PlanName.objects.all()

        self.assertTemplateUsed(response_to_test_template, 'main/delete.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(qs.count(), 0)

    def test_nonexistent_plan_view_DELETE(self):
        self.client.post('/login/', self.credentials, follow=True)

        response = self.client.post(
            reverse('delete-plan', args=[999]))

        self.assertTemplateUsed(response, 'errors/404.html')

    def test_plan_view_DELETE_another_user(self):
        self.client.post('/login/', self.credentials2)

        response = self.client.post(
            reverse('delete-plan', args=[self.plan_name.id]))

        qs = PlanName.objects.all()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(qs.count(), 1)

    def test_training_plan_view_POST(self):
        self.client.post('/login/', self.credentials, follow=True)

        training_name = TrainingName.objects.create(
            user=self.user,
            name="Training Test New"
        )
        plan_name = PlanName.objects.create(
            user=self.user,
            name="Plan Test New"
        )

        response = self.client.post('/add-training-to-plan/', data={
            'user': self.user,
            'name': plan_name,
            'training': training_name
        })

        response_to_test_template = self.client.get('/add-training-to-plan/')

        qs = Plan.objects.last()
        qs_all = Plan.objects.all()

        self.assertTemplateUsed(
            response_to_test_template, 'main/plan_form.html')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(qs_all.count(), 2)
        self.assertEqual(qs.training.name, "Training Test New")

    def test_training_plan_view_POST_with_incorrect_values(self):
        self.client.post('/login/', self.credentials, follow=True)

        response = self.client.post('/add-training-to-plan/', data={
            'user': self.user,
            'name': self.plan_name.id,
            'training': self.training_name.id
        })

        qs = Plan.objects.all()

        self.assertContains(response, "Error occured during")
        self.assertEqual(qs.count(), 1)

    def test_training_plan_view_DELETE(self):
        self.client.post('/login/', self.credentials, follow=True)

        response_to_test_template = self.client.get(
            reverse('delete-training-from-plan', args=[self.plan.id]))
        response = self.client.post(
            reverse('delete-training-from-plan', args=[self.plan.id]))

        qs = Plan.objects.all()

        self.assertTemplateUsed(response_to_test_template, 'main/delete.html')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(qs.count(), 0)

    def test_nonexistent_training_plan_view_DELETE(self):
        self.client.post('/login/', self.credentials)

        response = self.client.post(
            reverse('delete-training-from-plan', args=[999]))

        self.assertTemplateUsed(response, 'errors/404.html')

    def test_training_plan_view_DELETE_another_user(self):
        self.client.post('/login/', self.credentials2, follow=True)

        response = self.client.post(
            reverse('delete-training-from-plan', args=[self.plan.id]))

        qs = Plan.objects.all()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(qs.count(), 1)

    def test_trainings_view_GET(self):
        self.client.post('/login/', self.credentials)

        response = self.client.get('/training/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/training.html')

    def test_training_results_view_GET(self):
        self.client.post('/login/', self.credentials)

        response = self.client.get(
            reverse('training', args=[self.training_name.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/training_results.html')

    def test_training_results_view_GET_another_user(self):
        self.client.post('/login/', self.credentials2)

        response = self.client.get(
            reverse('training', args=[self.training_name.id]))

        self.assertEqual(response.status_code, 403)

    def test_nonexistent_training_results_view_GET(self):
        self.client.post('/login/', self.credentials)

        response = self.client.get(
            reverse('training', args=[999]))

        self.assertTemplateUsed(response, 'errors/404.html')

    def test_training_and_exercise_view_POST_without_earlier_create_training_name(self):
        self.client.post('/login/', self.credentials)

        response = self.client.post('/create-training/', follow=True, data={
            'user': self.user,
            'name': 'Training Test 1',
            'exercise': 'Training Exercise 1',
            'series': '',
            'reps': 12,
            'tempo': '2-1-2',
            'rir': 1,
            'rest': 90
        })
        response_to_test_template = self.client.get('/create-training/')

        qs_name = TrainingName.objects.last()
        qs_main = TrainingMain.objects.last()

        self.assertTemplateUsed(response_to_test_template,
                                'main/training_form.html')
        self.assertRedirects(response, '/training/')
        self.assertEqual(qs_name.name, 'Training Test 1')
        self.assertEqual(qs_main.exercise, 'Training Exercise 1')
        self.assertIsNone(qs_main.series)
        self.assertEqual(qs_main.tempo, '2-1-2')

    def test_create_training_without_authentication(self):
        url = reverse('create-training')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_training_and_exercise_view_POST_with_earlier_create_training_name(self):
        self.client.post('/login/', self.credentials)

        response = self.client.post('/create-training/', data={
            'user': self.user,
            'name': self.training_name.id,
            'exercise': 'Training Exercise 2'
        })

        qs = TrainingMain.objects.last()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(qs.exercise, 'Training Exercise 2')
        self.assertIsNone(qs.series)

    def test_training_and_exercise_view_POST_with_incorrect_values(self):
        self.client.post('/login/', self.credentials)

        try:
            self.client.post(reverse('create-training'), follow=True, data={
                'user': self.user,
                'name': self.training_name,
                'series': '',
                'reps': '',
                'tempo': '',
                'rir': '',
                'rest': '',
            })
        except:
            pass

    def test_training_view_UPDATE(self):
        self.client.post('/login/', self.credentials)

        response = self.client.post(reverse('update-training', args=[self.training_name.id]), follow=True, data={
            'name': 'Training Test XX'
        })
        response_to_test_template = self.client.get(
            reverse('update-training', args=[self.training_name.id]))

        qs = TrainingName.objects.get(id=self.training_name.id)

        self.assertTemplateUsed(
            response_to_test_template, 'main/create_form.html')
        self.assertRedirects(response, '/training/')
        self.assertEqual(qs.name, 'Training Test XX')

    def test_nonexistent_training_view_UPDATE(self):
        self.client.post('/login/', self.credentials)

        response = self.client.post(
            reverse('update-training', args=[999]), data={'name': 'Training Test New'})

        self.assertTemplateUsed(response, 'errors/404.html')

    def test_training_view_UPDATE_with_incorrect_values(self):
        self.client.post('/login/', self.credentials)

        TrainingName.objects.create(
            user=self.user,
            name="Training Test New"
        )

        response = self.client.post(reverse('update-training', args=[self.training_name.id]), follow=True, data={
            'name': 'Training Test New'
        })

        self.assertContains(response, "Error occured during create")

    def test_training_view_UPDATE_another_user(self):
        self.client.post('/login/', self.credentials2)

        response = self.client.post(reverse('update-training', args=[self.training_name.id]), follow=True, data={
            'name': 'Training Test DD'
        })

        qs = TrainingName.objects.get(id=self.training_name.id)

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(qs.name, 'Training Test DD')

    def test_training_view_DELETE(self):
        self.client.post('/login/', self.credentials)

        response_to_test_template = self.client.get(
            reverse('delete-training', args=[self.training_name.id]))

        self.assertTemplateUsed(response_to_test_template, 'main/delete.html')
        self.assertEqual(TrainingName.objects.all().count(), 1)

        response = self.client.post(
            reverse('delete-training', args=[self.training_name.id]), follow=True)

        qs = TrainingName.objects.all()

        self.assertRedirects(response, '/training/')
        self.assertEqual(qs.count(), 0)

    def test_training_view_DELETE_another_user(self):
        self.client.post('/login/', self.credentials2)

        response = self.client.post(
            reverse('delete-training', args=[self.training_name.id]), follow=True)

        qs = TrainingName.objects.all()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(qs.count(), 1)

    def test_nonexistent_training_view_DELETE(self):
        self.client.post('/login/', self.credentials)

        response = self.client.delete(
            reverse('delete-training', args=[999]))

        self.assertTemplateUsed(response, 'errors/404.html')

    def test_exercise_view_UPDATE(self):
        self.client.post('/login/', self.credentials)

        response_to_test_template = self.client.get(
            reverse('update-exercise', args=[self.training_main.id]))
        response = self.client.post(reverse('update-exercise', args=[self.training_main.id]), data={
            'exercise': 'new exercise',
            'series': '',
            'reps': 12,
            'tempo': '2-1-2',
            'rir': 1,
            'rest': 90
        })

        qs = TrainingMain.objects.get(id=self.training_main.id)

        self.assertTemplateUsed(
            response_to_test_template, 'main/training_form.html')
        self.assertRedirects(response, '/training/')
        self.assertIsNone(qs.series)
        self.assertEqual(qs.tempo, '2-1-2')

    def test_exercise_view_UPDATE_with_incorrect_data(self):
        self.client.post('/login/', self.credentials)

        TrainingMain.objects.create(
            user=self.user,
            name_id=self.training_name.pk,
            exercise="Exercise New")

        response = self.client.post(reverse('update-exercise', args=[self.training_main.id]), follow=True, data={
            'exercise': "Exercise New"
        })

        self.assertContains(response, "Error occured during")

    def test_nonexistent_exercise_view_UPDATE(self):
        self.client.post('/login/', self.credentials)

        response = self.client.post(reverse('update-exercise', args=[999]), data={
            'exercise': "Exercise New"
        })

        self.assertTemplateUsed(response, 'errors/404.html')

    def test_exercise_view_UPDATE_another_user(self):
        self.client.post('/login/', self.credentials2)

        response = self.client.post(reverse('update-exercise', args=[self.training_main.id]), follow=True, data={
            'series': 4
        })

        qs = TrainingMain.objects.get(id=self.training_main.id)

        self.assertEqual(response.status_code, 403)
        self.assertIsNone(qs.series)

    def test_exercise_view_DELETE(self):
        self.client.post('/login/', self.credentials)

        response_to_test_template = self.client.get(
            reverse('delete-exercise', args=[self.training_main.id]))
        response = self.client.post(
            reverse('delete-exercise', args=[self.training_main.id]), follow=True)

        qs = TrainingMain.objects.all()

        self.assertTemplateUsed(response_to_test_template, 'main/delete.html')
        self.assertRedirects(response, '/training/')
        self.assertEqual(qs.count(), 0)

    def test_nonexistent_exercise_view_DELETE(self):
        self.client.post('/login/', self.credentials)

        response = self.client.post(
            reverse('delete-exercise', args=[999]))

        self.assertTemplateUsed(response, 'errors/404.html')

    def test_exercise_view_DELETE_another_user(self):
        self.client.post('/login/', self.credentials2)

        response = self.client.post(
            reverse('delete-exercise', args=[self.training_main.id]), follow=True)

        qs = TrainingMain.objects.all()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(qs.count(), 1)

    def test_training_results_view_POST(self):
        self.client.post('/login/', self.credentials)

        response = self.client.post(reverse('create-exercise-score', args=[self.training_name.id]), data={
            'user': self.user,
            'name': self.training_name,
            'exercise': self.training_main,
            'series': 'Serie 1'
        })
        response_to_test_template = self.client.get(
            reverse('create-exercise-score', args=[self.training_name.id]))

        qs = TrainingResult.objects.last()

        self.assertTemplateUsed(response_to_test_template,
                                'main/training_result_form.html')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(qs.series, 'Serie 1')

    def test_training_results_view_POST_with_incorrect_values(self):
        self.client.post('/login/', self.credentials)

        response = self.client.post(reverse('create-exercise-score', args=[self.training_name.id]), follow=True, data={
            'user': self.user,
            'name': self.training_name,
            'exercise': "bad value",
            'series': 'Serie 1'
        })

        self.assertContains(response, "Error occured during")

    def test_training_results_view_UPDATE(self):
        self.client.post('/login/', self.credentials)

        response = self.client.post(reverse('update-exercise-score', args=[self.training_result.id]), data={
            'series': 'Serie 1'
        })
        response_to_test_template = self.client.get(
            reverse('update-exercise-score', args=[self.training_result.id]))

        qs = TrainingResult.objects.last()

        self.assertTemplateUsed(
            response_to_test_template, 'main/training_result_form.html')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(qs.series, 'Serie 1')

    def test_nonexistent_training_results_view_UPDATE(self):
        self.client.post('/login/', self.credentials)

        response = self.client.post(reverse('update-exercise-score', args=[999]), data={
            'series': 'Serie 1'
        })

        self.assertTemplateUsed(response, 'errors/404.html')

    def test_training_results_view_UPDATE_another_user(self):
        self.client.post('/login/', self.credentials2)

        response = self.client.post(reverse('update-exercise-score', args=[self.training_result.id]), data={
            'series': 'Serie 1'
        })

        qs = TrainingResult.objects.last()

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(qs.series, 'Serie 1')

    def test_training_results_view_DELETE(self):
        self.client.post('/login/', self.credentials)

        response_to_test_template = self.client.get(
            reverse('delete-exercise-score', args=[self.training_result.id]))
        response = self.client.post(
            reverse('delete-exercise-score', args=[self.training_result.id]))

        qs = TrainingResult.objects.all()

        self.assertTemplateUsed(
            response_to_test_template, 'main/delete.html')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(qs.count(), 0)

    def test_nonexistent_training_results_view_DELETE(self):
        self.client.post('/login/', self.credentials)

        response = self.client.post(
            reverse('delete-exercise-score', args=[999]))

        self.assertTemplateUsed(response, 'errors/404.html')

    def test_training_results_view_DELETE_another_user(self):
        self.client.post('/login/', self.credentials2)

        response = self.client.post(
            reverse('delete-exercise-score', args=[self.training_result.id]))

        qs = TrainingResult.objects.all()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(qs.count(), 1)
