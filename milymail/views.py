# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from milymail.forms import SendMailForm
from django.core.mail import EmailMessage

def index(request):
    if request.method == 'POST':
        form = SendMailForm(request.POST)
        if form.is_valid():
            #to_msg = request.POST.get('to_message')
            EmailMessage(request.POST.get('subject'),request.POST.get('message'),request.POST.get('from_message'),[request.POST.get('to_message')]).send()
            #print to_msg
            return HttpResponseRedirect('/')
    else:
        form = SendMailForm()
    return render(request,"index.html",{'form':form})

def home(request):
    return render(request, "base.html")
