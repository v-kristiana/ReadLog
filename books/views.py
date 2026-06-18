from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Avg
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Book, ReadingStatus, Favourite, Genre
from .forms import BookForm



@login_required
def toggle_favourite(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        if request.user.favourites.filter(book=book).exists():
            request.user.favourites.filter(book=book).delete()
        else:
            request.user.favourites.create(book=book)
    return redirect('books:book_detail', book_id=book_id)


@login_required
def set_reading_status(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    status = request.POST.get('status')
    if status:
        ReadingStatus.objects.update_or_create(
            user=request.user,
            book=book,
            defaults={'status': status}
        )
    return redirect('books:book_detail', book_id=book_id)


@login_required
def my_books(request):
    user_books = ReadingStatus.objects.filter(user=request.user).select_related('book')
    favourites = Favourite.objects.filter(user=request.user).select_related('book')
    return render(request, "books/my_books.html", {
        'user_books': user_books,
        'favourites': favourites,
    })


def user_can_manage_books(user):
    return user.is_authenticated and (user.is_staff or user.role in ['admin', 'worker'])


@login_required
def book_create(request):
    if not user_can_manage_books(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect('books:book_detail', book_id=book.id)
    else:
        form = BookForm()

    return render(request, 'books/add.html', {'form': form, 'action': 'Add Book'})


@login_required
def book_edit(request, book_id):
    if not user_can_manage_books(request.user):
        raise PermissionDenied

    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, 'books/book_form.html', {'form': form, 'action': 'Edit Book'})


@login_required
def book_delete(request, book_id):
    if not user_can_manage_books(request.user):
        raise PermissionDenied

    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('books:book_list')

    return render(request, 'books/book_confirm_delete.html', {'book': book})


def recommend_books_for_user(user, current_book=None, limit=5):
    qs = Book.objects.exclude(id=current_book.id) if current_book else Book.objects.all()

    genre_ids = []
    if user.is_authenticated:
        genre_ids = list(
            Genre.objects.filter(books__favourited_by__user=user)
                .annotate(count=Count('id'))
                .order_by('-count')
                .values_list('id', flat=True)[:3]
        )

    if not genre_ids and current_book is not None:
        genre_ids = list(current_book.genres.values_list('id', flat=True))

    if genre_ids:
        qs = qs.filter(genres__in=genre_ids).distinct()

    return qs.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:limit]

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()
    is_favourite = False
    current_status = None
    if request.user.is_authenticated:
        is_favourite = request.user.favourites.filter(book=book).exists()
        reading_status = request.user.reading_statuses.filter(book=book).first()
        current_status = reading_status.status if reading_status else None

    recommended_books = recommend_books_for_user(request.user, current_book=book)

    return render(request, "books/book_detail.html", {
        'book': book,
        'reviews': reviews,
        'is_favourite': is_favourite,
        'current_status': current_status,
        'status_choices': ReadingStatus.STATUS_CHOICES,
        'recommended_books': recommended_books,
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