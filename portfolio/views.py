from django.shortcuts import render

def index(request):
	return render(request, 'portfolio/index.html', {})
	
def about(request):
	return render(request, 'portfolio/about.html', {})
	
def career(request):
	return render(request, 'portfolio/career.html', {})
	
def projects(request):
    return render(request, 'portfolio/projects.html', {})
    
def contact(request):
    return render(request, 'portfolio/contact.html', {})