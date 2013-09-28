import logging

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.conf import settings


from oauth2client import xsrfutil

from .forms import SendMailForm
from .models import Credential
from contacts.models import get_contacts_for_user
from oauth2client.django_orm import Storage

import utils

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

@login_required
def home(request):
    credential = utils.get_user_credential(request.user)
    if credential is None or credential.invalid == True:
        settings.FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = settings.FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        contacts = get_contacts_for_user(request.user)
        return render(request, "home.html", locals())

@login_required
def auth_return(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'], request.user):
        return  HttpResponseBadRequest()
    credential = settings.FLOW.step2_exchange(request.REQUEST)
    storage = Storage(Credential, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/")

