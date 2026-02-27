from django.shortcuts import render


def landing(request):
    return render(request, 'countfree/landing.html')


def privacy(request):
    return render(request, 'countfree/privacy.html')


def support(request):
    return render(request, 'countfree/support.html')
