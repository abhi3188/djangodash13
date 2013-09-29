import logging

# Create your views here.
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.conf import settings
from oauth2client import xsrfutil
from .forms import SendMailForm
from .models import Credential
from django.template import RequestContext
from contacts.models import get_contacts_for_user,Contact,ContactEmail
from oauth2client.django_orm import Storage


def sign_in(request):
    return render(request, "sign_in.html", RequestContext(request))

def inbox(request):
    return render(request, "inbox.html", RequestContext(request))

def compose(request):
    return render(request, "compose.html")
    
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
    credential = Credential.objects.get_for_user(request.user)
    if credential is None or credential.invalid == True:
        settings.FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = settings.FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
#        mails = get_mails_for_user(request.user)
        contacts = get_contacts_for_user(request.user)
        Contact.objects.filter(user=request.user).delete()
        for contact in contacts:
            con=Contact.objects.create(user=request.user,provider_id=contact.id.text.split('/')[-1],name=contact.nickname,image_link=contact.GetPhotoLink())
            for email in contact.email:
                ContactEmail.objects.create(contact=con,email=email.address)
    return render(request, "home.html", locals())

@login_required
def auth_return(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'], request.user):
        return  HttpResponseBadRequest()
    credential = settings.FLOW.step2_exchange(request.REQUEST)
    storage = Storage(Credential, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/")

