from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile
from .models import Project


class ProjectCreationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.profile = Profile.objects.get(user=self.user)

    def test_create_project_assigns_logged_in_profile_as_owner(self):
        self.client.login(username='tester', password='secret123')

        response = self.client.post(reverse('create-project'), {
            'title': 'New Project',
            'description': 'A test project',
            'demo_link': '',
            'source_link': '',
        })

        self.assertEqual(response.status_code, 302)
        project = Project.objects.get(title='New Project')
        self.assertEqual(project.owner, self.profile)
