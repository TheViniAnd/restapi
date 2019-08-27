from django.shortcuts import render
from django.template import loader

# Create your views here.

def indexViews(request):
    """
    Представление для показа vue.js - приложения
    """
    return render(request, 'index.html', {})


