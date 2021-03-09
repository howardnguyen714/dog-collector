from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# home view
def home(request):
    return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')

def about(request):
    return HttpResponse('<h1>About the DogCollector</h1>')