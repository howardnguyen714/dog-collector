from django import forms
from .models import Feeding, Dog

class DogForm(forms.ModelForm):
  class Meta:
    model = Dog
    fields = ['name', 'breed', 'description', 'age']

class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'meal']