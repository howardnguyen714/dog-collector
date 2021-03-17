from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Dog, Walk
from .forms import FeedingForm, DogForm

# Create your views here.

# home view
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def dogs_index(request):
    dogs = Dog.objects.filter(user=request.user)
    return render(request, 'dogs/index.html', { 'dogs': dogs })

@login_required
def dogs_new(request):
  # create new instance of dog form filled with submitted values or nothing
  dog_form = DogForm(request.POST or None)
  # if the form was posted and valid
  if request.POST and dog_form.is_valid():
    # save new instance of a dog
    new_dog = dog_form.save(commit=False)
    new_dog.user = request.user
    new_dog.save()
    # redirect to index
    return redirect('index')
  else:
    # render the page with the new dog form
    return render(request, 'dogs/new.html', { 'dog_form': dog_form })

@login_required
def dogs_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    walks_dog_doesnt_have = Walk.objects.exclude(id__in = dog.walks.all().values_list('id'))
    feeding_form = FeedingForm()
    context = {
        'dog': dog,
        'feeding_form': feeding_form,
        'walks': walks_dog_doesnt_have
    }
    return render(request, 'dogs/detail.html', context)

@login_required
def add_feeding(request, dog_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.dog_id = dog_id
        new_feeding.save()
    return redirect('detail', dog_id=dog_id)

@login_required
def assoc_walk(request, walk_id, dog_id):
    # select a dog
    dog = Dog.objects.get(id=dog_id)
    # make the association
    dog.walks.add(walk_id)
    return redirect('detail', dog_id=dog_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
        # A GET or a bad POST request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)