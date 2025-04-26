from django.contrib import admin
from .models import Course, Review  # Mudamos de Disciplina, Feedback para Course, Review

admin.site.register(Course)
admin.site.register(Review)