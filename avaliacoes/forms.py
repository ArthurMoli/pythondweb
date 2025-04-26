from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'feedback', 'anonymous']
        widgets = {
            'rating': forms.RadioSelect(),
            'feedback': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Share your experience with this course...'
            }),
        }
        labels = {
            'rating': 'How would you rate this course?',
            'feedback': 'Your feedback',
            'anonymous': 'Submit anonymously'
        }
        help_texts = {
            'anonymous': 'Your name will not be visible to other students if checked'
        }