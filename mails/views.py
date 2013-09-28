# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage

from .forms import SendMailForm

def index(request):
    if request.method == 'POST':
        form = SendMailForm(request.POST,request.FILES)
        if form.is_valid():
            #to_msg = request.POST.get('to_message')
            upload_file = request.FILES['upload']
            message=EmailMessage(request.POST.get('subject'),request.POST.get('message'),request.POST.get('from_message'),[request.POST.get('to_message')],headers={'Reply-to':request.POST.get('from_message')})
            message.attach(upload_file.name,upload_file.read(),upload_file.content_type)
            message.send()
            #print to_msg
            return HttpResponseRedirect('/')
    else:
        form = SendMailForm()
    return render(request,"index.html",{'form':form})

def home(request):
    return render(request, "base.html")