from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from books.models import Book
from .models import Review
from .forms import ReviewForm

@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect('books:book_detail', book_id=book_id)
    else:
        form = ReviewForm()
    return render(request, "reviews/add_review.html", {'form': form, 'book': book})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    can_delete = (
        request.user == review.user or
        request.user.is_staff or
        getattr(request.user, 'role', None) in ['admin', 'worker']
    )
    if not can_delete:
        raise PermissionDenied

    if request.method == 'POST':
        book_id = review.book.id
        review.delete()
        return redirect('books:book_detail', book_id=book_id)

    return redirect('books:book_detail', book_id=review.book.id)
