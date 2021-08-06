import os
import re
import tempfile
import rango.models
from rango import forms
from populate_script import populate
from datetime import datetime, timedelta
from rango.models import Category, Page
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

def create_user_object():

    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user

def create_super_user_object():

    return User.objects.create_superuser('admin', 'admin@test.com', 'testpassword')

class Test_Config(TestCase):

    def test_middleware_present(self):

        self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE)
    
    def test_session_app_present(self):

        self.assertTrue('django.contrib.sessions' in settings.INSTALLED_APPS)


class Test_Pages_Display(TestCase):

    def setUp(self):
        populate()
        self.response = self.client.get(reverse('rango:index'))
        self.content = self.response.content.decode()
    
    def test_template_filename(self):

        self.assertTemplateUsed(self.response, 'rango/index.html', f"{FAILURE_HEADER}Are you using index.html for your index() view? Why not?!{FAILURE_FOOTER}")

    def test_index_context_dictionary(self):

        expected_pages_order = list(Page.objects.order_by('-rating')) 

        self.assertTrue('pages' in self.response.context, f"{FAILURE_HEADER}We couldn't find a 'pages' variable in the index() view's context dictionary. Did you complete the Chapter 6 exercises?{FAILURE_FOOTER}")
        self.assertEqual(expected_pages_order, list(self.response.context['pages']), f"{FAILURE_HEADER}The 'pages' context dictionary variable for the index() view didn't return the QuerySet we were expectecting: got {list(self.response.context['pages'])}, expected {expected_pages_order}. Did you apply the correct ordering to the filtered results?{FAILURE_FOOTER}")
    
class Test_User_Profile(TestCase):

    def test_userprofile_class(self):

        self.assertTrue('UserProfile' in dir(rango.models))

        user_profile = rango.models.UserProfile()

        # Now check that all the required attributes are present.
        # We do this by building up a UserProfile instance, and saving it.
        expected_attributes = {
            'website': 'www.google.com',
            'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name,
            'user': create_user_object(),
        }

        expected_types = {
            'website': models.fields.URLField,
            'picture': models.fields.files.ImageField,
            'user': models.fields.related.OneToOneField,
        }

        found_count = 0

        for attr in user_profile._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserProfile model.{FAILURE_FOOTER}")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])
        
        self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}In the UserProfile model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. Check your implementation and try again.{FAILURE_FOOTER}")
        user_profile.save()
    

    def test_model_admin_interface_inclusion(self):

        super_user = create_super_user_object()
        self.client.login(username='admin', password='testpassword')

        # The following URL should be available if the UserProfile model has been registered to the admin interface.
        response = self.client.get('/admin/rango/userprofile/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When attempting to access the UserProfile in the admin interface, we didn't get a HTTP 200 status code. Did you register the new model with the admin interface?{FAILURE_FOOTER}")
