from django.shortcuts import render

def index(request):
    return render(request, 'portfolio/modern_index.html', {})