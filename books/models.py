from django.db import models

from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)


class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favourites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favourited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user} - {self.book}"


class ReadingStatus(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Plānots'),
        ('reading', 'Lasu'),
        ('read', 'Izlasīts'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reading_statuses')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_statuses')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='planned')

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user} - {self.book} - {self.status}"