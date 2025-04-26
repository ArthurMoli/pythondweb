from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/review/', views.submit_review, name='submit_review'),
    path('courses/<int:course_id>/edit-review/', views.edit_review, name='edit_review'),
    path('courses/<int:course_id>/delete-review/', views.delete_review, name='delete_review'),
]