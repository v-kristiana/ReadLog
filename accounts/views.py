from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import RegisterForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('books:book_list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    favourites = request.user.favourites.all()
    reading_statuses = request.user.reading_statuses.all()
    return render(request, 'accounts/profile.html', {
        'favourites': favourites,
        'reading_statuses': reading_statuses,
    })


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('books:book_list')