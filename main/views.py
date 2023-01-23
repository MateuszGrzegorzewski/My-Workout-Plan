from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Training, TrainingMain, TrainingName, Plan, PlanName
from .forms import TrainingForm, TrainingMainForm, TrainingNameForm, PlanNameForm, PlanForm


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
               'plans': plans,
               "trainings": trainings
               }

    return render(request, 'main/plan.html', context)


@login_required(login_url="login")
def training(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    trainings_name = TrainingName.objects.filter(
        name__icontains=q).filter(user=request.user)
    trainings_main = TrainingMain.objects.filter(user=request.user)

    context = {'trainings_name': trainings_name,
               "trainings_main": trainings_main,
               }

    return render(request, 'main/training.html', context)


@login_required(login_url="login")
def training_pk(request, pk):
    trainings_name = TrainingName.objects.get(id=pk)
    trainings_main = trainings_name.trainingmain_set.all()
    training = trainings_name.training_set.all()

    if request.user != trainings_name.user:
        return HttpResponse("You have not permissions.")

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

    context = {'form': form, "trainings": trainings, 'page': page}
    return render(request, 'main/training_form.html', context)

    # Poszukać jak rozwiązać problem integerfielda


@login_required(login_url="login")
def updateTraining(request, pk):
    training_name = TrainingName.objects.get(id=pk)
    form = TrainingNameForm(instance=training_name)
    # I change this for create bbecause i do not know to redirect to another site
    if request.user != training_name.user:
        return HttpResponse("You have not permissions.")

    if request.method == 'POST':
        form = TrainingNameForm(request.POST, instance=training_name)
        if form.is_valid():
            form.save()
            return redirect('training')

    context = {'form': form}
    return render(request, 'main/create_form.html', context)


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
def updateExercise(request, pk):
    training = TrainingMain.objects.get(id=pk)
    form = TrainingMainForm(instance=training)

    if request.user != training.user:
        return HttpResponse("You have not permissions.")

    if request.method == 'POST':
        series = request.POST.get('series')
        if series == "":
            series = None

        training.series = series
        training.reps = request.POST.get('reps')
        training.tempo = request.POST.get('tempo')
        training.rir = request.POST.get('rir')
        training.rest = request.POST.get('rest')
        training.save()

        return redirect('training')

    context = {'form': form, "training": training}
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
def createExerciseScores(request, pk_training):
    page = 'create'
    training = TrainingName.objects.get(id=pk_training)
    form = TrainingForm()
    exercises = training.trainingmain_set.all()

    if request.method == 'POST':
        exercise_req = request.POST.get('exercise')
        exercise = TrainingMain.objects.filter(
            user=request.user).filter(name=training).get(exercise=exercise_req)

        integers = ["weight", "reps", "rir"]
        values = [None if request.POST.get(i) == ""
                  else request.POST.get(i) for i in integers]

        Training.objects.create(
            user=request.user,
            name=training,
            exercise=exercise,
            series=request.POST.get('series'),
            weight=values[0],
            reps=values[1],
            rir=values[2],
        )

        return redirect('training', pk=training.id)

    context = {'page': page, 'form': form,
               "training": training, "exercises": exercises}

    return render(request, 'main/training_result_form.html', context)


@login_required(login_url="login")
def updateExerciseScores(request, pk):
    training_result = Training.objects.get(id=pk)
    form = TrainingForm(instance=training_result)

    if request.user != training_result.user:
        return HttpResponse("You have not permissions.")

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
    training_result = Training.objects.get(id=pk)

    if request.user != training_result.user:
        return HttpResponse("You have not permissions.")

    if request.method == 'POST':
        training_result.delete()
        return redirect('training', pk=training_result.name.id)

    context = {
        "obj": f"{training_result} for excercise: {training_result.exercise} in training: {training_result.name}"
    }

    return render(request, 'main/delete.html', context)


#  !!!

# NOW THIS TO IMPORVE

#  !!!


@login_required(login_url="login")
def createPlan(request):
    form = PlanNameForm()

    if request.method == 'POST':
        PlanName.objects.create(
            user=request.user,
            name=request.POST.get('name')
        )

        return redirect('plan')

    context = {'form': form}
    return render(request, 'main/plan_main_form.html', context)


@login_required(login_url="login")
def updatePlan(request, pk):
    plan = PlanName.objects.get(id=pk)
    form = PlanNameForm(instance=plan)

    if request.user != plan.user:
        return HttpResponse("You have not permissions.")

    if request.method == 'POST':
        form = PlanNameForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('plan')

    context = {'form': form}
    return render(request, 'main/create_form.html', context)


@login_required(login_url="login")
def deletePlan(request, pk):
    plan = PlanName.objects.get(id=pk)

    if request.user != plan.user:
        return HttpResponse("You have not permissions.")

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
        name_plan = PlanName.objects.filter(user=request.user).get(name=name)

        training = request.POST.get('training')
        training_name = TrainingName.objects.filter(
            user=request.user).get(name=training)

        Plan.objects.create(
            user=request.user,
            name=name_plan,
            training=training_name
        )
        return redirect('plan')

    context = {'form': form, "plans": plans, "trainings": trainings}
    return render(request, 'main/plan_form.html', context)


@login_required(login_url="login")
def deleteTrainingFromPlan(request, pk):
    plan = Plan.objects.get(id=pk)

    if request.user != plan.user:
        return HttpResponse("You have not permissions.")

    if request.method == 'POST':
        plan.delete()
        return redirect('plan')

    return render(request, 'main/delete.html', {"obj": plan.training.name})


#  sprawdzić get_or_error albo coś do tych wszystkich errorów
