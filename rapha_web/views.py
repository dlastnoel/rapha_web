from urllib import response
from django.shortcuts import render, redirect
from . forms import ContactForm
from django.core.mail import send_mail
# Create your views here.


def index(request):
    form = ContactForm()
    if(request.user.is_authenticated):
        return redirect('dashboard')
    context = {
        'title': 'Your Medical Friend',
        'form': form
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

def sendEmail(request):
  form = ContactForm(request.POST)
  if form.is_valid():
    name = form.cleaned_data['name']
    subject = form.cleaned_data['subject']
    from_email = form.cleaned_data['from_email']
    message = form.cleaned_data['message']
    full_message = 'from: ' + from_email + ' (' +  name + ') ' + message
    try:
      send_mail(subject, full_message, from_email, [
                'raphacodesecret@gmail.com'])
    except :
      print('error')
  else:
    print('FORM INVALID')
  return redirect('index')
