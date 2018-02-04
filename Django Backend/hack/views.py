from django.http import HttpResponse
from django.shortcuts import render_to_response,render, redirect
from hack.forms import Industry
from keras.models import model_from_json
from sklearn.externals import joblib

def home(request):
    if request.method == 'POST':
        form = Industry(request.POST)
        if form.is_valid():
            choice = form.cleaned_data.get('choice')
        print(choice)

    else:
        form = Industry()

    return render(request, "index.html", {'form': form})

def index(request):
    return(render(request, "indexold.html"))