from django.http import HttpRequest
from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model

from testapp.models import MosTest
from testapp.views import top

UserModel = get_user_model()

# Create your tests here.
class TopPageRenderTestappTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="top_secret_pass0001",
        )
        self.test = MosTest.objects.create(
            title="test_title",
            created_by=self.user,
        )

    def test_should_return_test_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.test.title)

    def test_should_return_username(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)



class TopPageViewTest(TestCase):
    def test_top_returns_200_and_expected_title(self):
        response = self.client.get("/")
        self.assertContains(response, "Top", status_code=200)

    def test_top_returns_expected_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "test/top.html")


