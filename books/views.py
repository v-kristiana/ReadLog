from django.shortcuts import render
from .models import Book
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()
    return render(request, "books/book_detail.html", {
        'book': book,
        'reviews': reviews,
    })

def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {
        'books': books,
    })

def search_books(request):
    query = request.GET.get('q', '')
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genres__name__icontains=query)
        ).distinct()
    return render(request, "books/search_results.html", {
        'books': books,
        'query': query,
    })