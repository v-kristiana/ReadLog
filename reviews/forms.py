from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'placeholder': 'Rating (1-5)'})
        self.fields['comment'].widget.attrs.update({'placeholder': 'Share your thoughts...'})
