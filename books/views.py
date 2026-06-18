from django.shortcuts import render
from .models import Book
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import ReadingStatus


@login_required
def toggle_favourite(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        if request.user.favourites.filter(book=book).exists():
            request.user.favourites.filter(book=book).delete()
        else:
            request.user.favourites.create(book=book)
    return redirect('book_detail', book_id=book_id)


@login_required
def set_reading_status(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    status = request.POST.get('status')
    if status:
        try:
            reading_status = request.user.reading_statuses.get(book=book)
            reading_status.status = status
            reading_status.save()
        except ReadingStatus.DoesNotExist:
            ReadingStatus.objects.create(user=request.user, book=book, status=status)
    return redirect('book_detail', book_id=book_id)




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