from django.urls import path

from . import views

urlpatterns = [
    path("stat", views.stats, name="stat_view"),
    path("test_results", views.test_result_list, name="test_result_list_view"),
    path("test_result", views.test_result_post, name="post_test_result_view"),
    path("test_result/<pk>", views.test_result_delete, name="delete_test_result_view"),
]
