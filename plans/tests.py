from django.test import TestCase
import os
# djjango.conf setting. it is possible to get all settings e.g. settings.SECRET_KEY
# from django.conf import settings
from django.contrib.auth.password_validation import validate_password


# class TryDjangoConfigTest(TestCase):
#     def test_secret_key_strength(self):
#         def test_secret_key_strength(self):
#             SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
#             try:
#                 is_strong = validate_password(SECRET_KEY)
#             except Exception as e:
#                 msg = f'Weak Secret Key {e.messages}'
#                 self.fail(msg)
