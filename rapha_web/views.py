from django.shortcuts import render, redirect
# Create your views here.


def index(request):
    if(request.user.is_authenticated):
        return redirect('dashboard')
    context = {
        'title': 'Your Medical Friend',
    }
    return render(request, 'index.html', context)


def download(request):
    if(request.user.is_authenticated):
        return redirect('dashboard')
    context = {
        'title': 'Download',
        'is_download': True
    }
    return render(request, 'download.html', context)
