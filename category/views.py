from django.shortcuts import render
from django.http import HttpResponse
from .models import Category 
from .models import models
from store.models import Product


# Create your views here.
def home(request):
    return render(request,'index.html')

