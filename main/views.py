from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.http import Http404

from .forms import (PlanForm, PlanNameForm, TrainingMainForm, TrainingNameForm,
                    TrainingResultForm)
from .models import Plan, PlanName, TrainingMain, TrainingName, TrainingResult


def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})


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


@login_required(login_url="login")
def plan(request):
    plan_names = PlanName.objects.filter(user=request.user)
    plans = Plan.objects.filter(user=request.user)
    trainings = TrainingMain.objects.filter(user=request.user)

    context = {"plan_names": plan_names,
               "plans": plans,
               "trainings": trainings
               }

    return render(request, 'main/plan.html', context)


@login_required(login_url="login")
def trainings(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    trainings_name = TrainingName.objects.filter(
        name__icontains=q).filter(user=request.user)
    trainings_main = TrainingMain.objects.filter(user=request.user)

    context = {'trainings_name': trainings_name,
               "trainings_main": trainings_main,
               }

    return render(request, 'main/training.html', context)


@login_required(login_url="login")
def training(request, pk):
    try:
        trainings_name = TrainingName.objects.get(id=pk)
    except:
        raise Http404
    trainings_main = trainings_name.trainingmain_set.all()
    training = trainings_name.trainingresult_set.all()

    if request.user != trainings_name.user:
        raise PermissionDenied

    context = {'trainings_name': trainings_name,
               "trainings_main": trainings_main,
               "training": training
               }

    return render(request, 'main/training_results.html', context)


@login_required(login_url="login")
def createTraining(request):
    page = 'create'
    form = TrainingMainForm()
    trainings = TrainingName.objects.filter(user=request.user)

    if request.method == 'POST':
        training_name = request.POST.get('name')
        training, created = TrainingName.objects.filter(user=request.user).get_or_create(
            name=training_name, defaults={"user": request.user, "name": training_name})

        series = request.POST.get('series')
        if series == "":
            series = None

        try:
            TrainingMain.objects.create(
                user=request.user,
                name=training,
                exercise=request.POST.get('exercise'),
                series=series,
                reps=request.POST.get('reps'),
                tempo=request.POST.get('tempo'),
                rir=request.POST.get('rir'),
                rest=request.POST.get('rest'),
            )
            return redirect('training')
        except:
            messages.error(request, """Error occured during create Training.
                    The likely cause is an attempt to create the same exercise.""")

    context = {'form': form, "trainings": trainings, 'page': page}
    return render(request, 'main/training_form.html', context)


@login_required(login_url="login")
def updateTraining(request, pk):
    try:
        training_name = TrainingName.objects.get(id=pk)
    except:
        raise Http404
    form = TrainingNameForm(instance=training_name)

    if request.user != training_name.user:
        raise PermissionDenied

    if request.method == 'POST':
        try:
            form = TrainingNameForm(request.POST, instance=training_name)
            if form.is_valid():
                form.save()
                return redirect('training')
        except:
            messages.error(request, """Error occured during create Training.
                    The likely cause is an attempt to create the same training.""")

    context = {'form': form}
    return render(request, 'main/create_form.html', context)


@login_required(login_url="login")
def deleteTraining(request, pk):
    try:
        training_name = TrainingName.objects.get(id=pk)
    except:
        raise Http404

    if request.user != training_name.user:
        raise PermissionDenied

    if request.method == 'POST':
        training_name.delete()
        return redirect('training')

    return render(request, 'main/delete.html', {"obj": training_name})


@login_required(login_url="login")
def updateExercise(request, pk):
    try:
        training = TrainingMain.objects.get(id=pk)
    except:
        raise Http404
    form = TrainingMainForm(instance=training)

    if request.user != training.user:
        raise PermissionDenied

    if request.method == 'POST':
        try:
            series = request.POST.get('series')
            if series == "":
                series = None

            training.exercise = request.POST.get('exercise')
            training.series = series
            training.reps = request.POST.get('reps')
            training.tempo = request.POST.get('tempo')
            training.rir = request.POST.get('rir')
            training.rest = request.POST.get('rest')
            training.save()
            return redirect('training')
        except:
            messages.error(request, """Error occured during updating Training.
                    The likely cause is an attempt to create the same exercise.""")

    context = {'form': form, "training": training}
    return render(request, 'main/training_form.html', context)


@login_required(login_url="login")
def deleteExercise(request, pk):
    try:
        training = TrainingMain.objects.get(id=pk)
    except:
        raise Http404

    if request.user != training.user:
        raise PermissionDenied

    if request.method == 'POST':
        training.delete()
        return redirect('training')

    return render(request, 'main/delete.html', {"obj": training})


@login_required(login_url="login")
def createExerciseScores(request, pk_training):
    page = 'create'
    training = TrainingName.objects.get(id=pk_training)
    form = TrainingResultForm()
    exercises = training.trainingmain_set.all()

    if request.method == 'POST':
        exercise_req = request.POST.get('exercise')
        try:
            exercise = TrainingMain.objects.filter(
                user=request.user).filter(name=training).get(exercise=exercise_req)
        except:
            pass

        integers = ["weight", "reps", "rir"]
        values = [None if request.POST.get(i) == ""
                  else request.POST.get(i) for i in integers]
        try:
            TrainingResult.objects.create(
                user=request.user,
                name=training,
                exercise=exercise,
                series=request.POST.get('series'),
                weight=values[0],
                reps=values[1],
                rir=values[2],
            )
            return redirect('training', pk=training.id)
        except:
            messages.error(request, """Error occured during create score of training.
                                    The likely cause is an attempt to add exercise or training which does not exist.""")

    context = {'page': page, 'form': form,
               "training": training, "exercises": exercises}

    return render(request, 'main/training_result_form.html', context)


@login_required(login_url="login")
def updateExerciseScores(request, pk):
    try:
        training_result = TrainingResult.objects.get(id=pk)
    except:
        raise Http404
    form = TrainingResultForm(instance=training_result)

    if request.user != training_result.user:
        raise PermissionDenied

    if request.method == 'POST':

        integers = ["weight", "reps", "rir"]
        values = [None if request.POST.get(i) == ""
                  else request.POST.get(i) for i in integers]

        training_result.series = request.POST.get('series')
        training_result.weight = values[0]
        training_result.reps = values[1]
        training_result.rir = values[2]
        training_result.save()

        return redirect('training', pk=training_result.name.id)

    context = {'form': form, 'training_result': training_result}
    return render(request, 'main/training_result_form.html', context)


@login_required(login_url="login")
def deleteExerciseScores(request, pk):
    try:
        training_result = TrainingResult.objects.get(id=pk)
    except:
        raise Http404

    if request.user != training_result.user:
        raise PermissionDenied

    if request.method == 'POST':
        training_result.delete()
        return redirect('training', pk=training_result.name.id)

    context = {
        "obj": f"{training_result} for excercise: {training_result.exercise} in training: {training_result.name}"
    }

    return render(request, 'main/delete.html', context)


@login_required(login_url="login")
def createPlan(request):
    form = PlanNameForm()

    try:
        if request.method == 'POST':
            PlanName.objects.create(
                user=request.user,
                name=request.POST.get('name')
            )
            return redirect('plan')
    except:
        messages.error(
            request, """Error occured during create plan. 
                    The likely cause is an attempt to make the same name for the plan.""")

    context = {'form': form}
    return render(request, 'main/plan_main_form.html', context)


@login_required(login_url="login")
def updatePlan(request, pk):
    try:
        plan = PlanName.objects.get(id=pk)
    except:
        raise Http404
    form = PlanNameForm(instance=plan)

    if request.user != plan.user:
        raise PermissionDenied

    try:
        if request.method == 'POST':
            form = PlanNameForm(request.POST, instance=plan)
            if form.is_valid():
                form.save()
                return redirect('plan')
    except:
        messages.error(
            request, """Error occured during create plan. 
                    The likely cause is an attempt to make the same name for the plan.""")

    context = {'form': form}
    return render(request, 'main/create_form.html', context)


@login_required(login_url="login")
def deletePlan(request, pk):
    try:
        plan = PlanName.objects.get(id=pk)
    except:
        raise Http404

    if request.user != plan.user:
        raise PermissionDenied

    if request.method == 'POST':
        plan.delete()
        return redirect('plan')

    return render(request, 'main/delete.html', {"obj": plan})


@login_required(login_url="login")
def addTrainingToPlan(request):
    form = PlanForm()
    plans = PlanName.objects.filter(user=request.user)
    trainings = TrainingName.objects.filter(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        training = request.POST.get('training')

        try:
            name_plan = PlanName.objects.filter(
                user=request.user).get(name=name)
            training_name = TrainingName.objects.filter(
                user=request.user).get(name=training)
        except:
            pass

        try:
            Plan.objects.create(
                user=request.user,
                name=name_plan,
                training=training_name
            )
            return redirect('plan')
        except:
            messages.error(
                request, """Error occured during adding training to plan. Possible caues: 
                        1. Plan or training does not exist  
                        2. Attempting to add the same training to the plan is impossible""")

    context = {'form': form, "plans": plans, "trainings": trainings}
    return render(request, 'main/plan_form.html', context)


@login_required(login_url="login")
def deleteTrainingFromPlan(request, pk):
    try:
        plan = Plan.objects.get(id=pk)
    except:
        raise Http404

    if request.user != plan.user:
        raise PermissionDenied

    if request.method == 'POST':
        plan.delete()
        return redirect('plan')

    return render(request, 'main/delete.html', {"obj": plan.training.name})
