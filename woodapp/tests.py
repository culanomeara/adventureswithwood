from django.test import TestCase


class TestHomeViews(TestCase):
    """
    A class for testing the home page views
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
    A class for testing posts views
    """
    def test_get_posts_page(self):
        """
        This test checks if the posts page is displayed
        """
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')


class TestProjectsViews(TestCase):
    """
    A class for testing projects views
    """
    def test_get_projects_page(self):
        """
        This test checks if the projects page is displayed
        """
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects.html')
