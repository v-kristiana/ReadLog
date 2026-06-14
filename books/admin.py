from django.contrib import admin
from .models import Genre, Book, Favourite, ReadingStatus

admin.site.register(Genre)
admin.site.register(Favourite)
admin.site.register(ReadingStatus)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'average_rating')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('genres',)