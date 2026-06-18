from django import forms
from .models import Book, Genre

class BookForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'year', 'isbn', 'image', 'genres']
