from django.urls import path

from testapp import views

urlpatterns = [
    path("new_test/", views.test_new, name="test_new"),
    path("<int:test_id>/", views.test_detail, name="test_detail"),
    path("<int:test_id>/edit/", views.test_edit, name="test_edit"),
    path("<int:test_id>/delete/", views.test_delete, name="test_delete"),
    path("get_new_form/", views.get_new_form, name="get_new_form"),
]