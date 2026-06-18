from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/<int:book_id>/', views.add_review, name='add_review'),
    path('<int:review_id>/delete/', views.delete_review, name='delete_review'),
]
