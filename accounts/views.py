from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.error(request, "Username or password does not exist")

    return render(request, 'accounts/login.html')


def logoutPage(request):
    logout(request)
    return redirect(reverse('login'))


def registerPage(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
        messages.error(
            request, "Unsuccessful registration. Invalid information.")

    form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})
