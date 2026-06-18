from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from books.models import Book
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