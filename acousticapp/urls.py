
from django.urls import path
from acousticapp import views


urlpatterns = [
    path("<int:test_id>/answer_new/", views.answer_new, name="answer_new"),
    path("<int:test_id>/result/", views.result, name="result"),
]