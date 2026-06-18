import os
from urllib.parse import urlparse

import requests
from django import forms
from django.core.files.base import ContentFile
from .models import Book, Genre

class BookForm(forms.ModelForm):
    image_url = forms.URLField(required=False, label='Image URL')
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'year', 'isbn', 'image', 'image_url', 'genres']

    def save(self, commit=True):
        book = super().save(commit=False)
        image_url = self.cleaned_data.get('image_url')
        image_file = self.cleaned_data.get('image')

        if image_url and not image_file:
            try:
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()
                parsed_url = urlparse(image_url)
                filename = os.path.basename(parsed_url.path) or 'cover.jpg'
                if not os.path.splitext(filename)[1]:
                    filename += '.jpg'
                book.image.save(filename, ContentFile(response.content), save=False)
            except Exception:
                pass

        if commit:
            book.save()
            self.save_m2m()

        return book
