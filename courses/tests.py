from django.test import TestCase, Client


class TestRedirection(TestCase):
    def testDefaultPageLoading(self):
        client = Client()
        response = client.get('')
        self.assertTemplateUsed(response, "courses/course/list.html", "correct template is loaded")
