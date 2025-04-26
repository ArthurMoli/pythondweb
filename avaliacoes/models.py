from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Course(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    instructor = models.CharField(max_length=100)
    semester = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    
    def average_rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg'] or 0
    
    def total_reviews(self):
        return self.review_set.count()

    def __str__(self):
        return f"{self.code} - {self.title}"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    feedback = models.TextField(blank=True)
    anonymous = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('course', 'student')
        ordering = ['-date_submitted']

    def __str__(self):
        return f"{self.course.title} - {self.student.username} ({self.rating}⭐)"