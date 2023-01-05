from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Training, TrainingMain, TrainingName, Plan
from .forms import TrainingForm, TrainingMainForm, TrainingNameForm


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')

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
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist")

    context = {"page": page}
    return render(request, 'main/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")

    form = UserCreationForm()

    return render(request, 'main/login_register.html', {'form': form})


def home(request):
    return render(request, 'main/home.html')


def plan(request):
    plans = Plan.objects.all()
    trainings_name = TrainingName.objects.all()
    trainings_main = TrainingMain.objects.all()
    context = {'plans': plans,
               'trainings_name': trainings_name,
               "trainings_main": trainings_main
               }
    # tutaj napewno do zmiany context i wartości, żeby dobrze po get wybierać
    return render(request, 'main/plan.html', context)


@login_required(login_url="login")
def training(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    trainings_name = TrainingName.objects.filter(name__icontains=q)
    trainings_main = TrainingMain.objects.all()
    context = {'trainings_name': trainings_name,
               "trainings_main": trainings_main,
               }

    return render(request, 'main/training.html', context)


@login_required(login_url="login")
def training_pk(request, pk):
    trainings_name = TrainingName.objects.get(id=pk)
    trainings_main = TrainingMain.objects.all()
    training = Training.objects.all()

    if request.user != trainings_name.user:
        return HttpResponse("You have not permissions.")

    context = {'trainings_name': trainings_name,
               "trainings_main": trainings_main,
               "training": training
               }

    return render(request, 'main/training_pk.html', context)


@login_required(login_url="login")
def createTraining(request):
    form = TrainingNameForm()
    if request.method == 'POST':
        form = TrainingNameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training')

    context = {'form': form}
    return render(request, 'main/training_form.html', context)


@login_required(login_url="login")
def updateTraining(request, pk):
    training_name = TrainingName.objects.get(id=pk)
    form = TrainingNameForm(instance=training_name)

    if request.user != training_name.user:
        return HttpResponse("You have not permissions.")

    if request.method == 'POST':
        form = TrainingNameForm(request.POST, instance=training_name)
        if form.is_valid():
            form.save()
            return redirect('training')

    context = {'form': form}
    return render(request, 'main/training_form.html', context)


@login_required(login_url="login")
def deleteTraining(request, pk):
    training_name = TrainingName.objects.get(id=pk)

    if request.user != training_name.user:
        return HttpResponse("You have not permissions.")

    if request.method == 'POST':
        training_name.delete()
        return redirect('training')

    return render(request, 'main/delete.html', {"obj": training_name})


@login_required(login_url="login")
def createExercise(request):
    form = TrainingMainForm()
    if request.method == 'POST':
        form = TrainingMainForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training')

    context = {'form': form}
    return render(request, 'main/training_form.html', context)


@login_required(login_url="login")
def updateExercise(request, pk):
    training = TrainingMain.objects.get(id=pk)
    form = TrainingMainForm(instance=training)

    if request.user != training.user:
        return HttpResponse("You have not permissions.")

    if request.method == 'POST':
        form = TrainingMainForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            return redirect('training')

    context = {'form': form}
    return render(request, 'main/training_form.html', context)


@login_required(login_url="login")
def deleteExercise(request, pk):
    training = TrainingMain.objects.get(id=pk)

    if request.user != training.user:
        return HttpResponse("You have not permissions.")

    if request.method == 'POST':
        training.delete()
        return redirect('training')

    return render(request, 'main/delete.html', {"obj": training})


@login_required(login_url="login")
def createExerciseScores(request):
    form = TrainingForm()
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training', pk=training_pk.name.id)

    context = {'form': form}
    return render(request, 'main/training_form.html', context)


@login_required(login_url="login")
def updateExerciseScores(request, pk):
    training_pk = Training.objects.get(id=pk)
    form = TrainingForm(instance=training_pk)

    if request.user != training_pk.user:
        return HttpResponse("You have not permissions.")

    if request.method == 'POST':
        form = TrainingForm(request.POST, instance=training_pk)
        if form.is_valid():
            form.save()
            return redirect('training', pk=training_pk.name.id)

    context = {'form': form}
    return render(request, 'main/training_form.html', context)


@login_required(login_url="login")
def deleteExerciseScores(request, pk):
    training_pk = Training.objects.get(id=pk)

    if request.user != training_pk.user:
        return HttpResponse("You have not permissions.")

    if request.method == 'POST':
        training_pk.delete()
        return redirect('training', pk=training_pk.name.id)

    return render(request, 'main/delete.html', {"obj": training_pk})
