from django.test import TestCase


class TestHomeViews(TestCase):
    """
    A class for testing the home page view
    """
    def test_get_home_page(self):
        """
        This test checks if the home page is displayed properly
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class TestPostsViews(TestCase):
    """
    A class for testing posts view
    """
    def test_get_posts_page(self):
        """
        This test checks if the posts page is displayed properly
        """
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')


class TestProjectsViews(TestCase):
    """
    A class for testing projects view
    """
    def test_get_projects_page(self):
        """
        This test checks if the projects page is displayed properly
        """
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects.html')


class TestProjectCreateView(TestCase):
    """
    A class for testing project create view
    """
    def test_get_project_create_page(self):
        """
        This test checks if the project create page is displayed properly
        """
        response = self.client.get('/projects_create')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects_create.html')
