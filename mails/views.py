import logging

# Create your views here.
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template import RequestContext

from oauth2client import xsrfutil
from oauth2client.django_orm import Storage

import utils
from .models import MiliBox, Credential
from .forms import SendMailForm
from contacts.models import get_contacts_for_user,Contact,ContactEmail

def sign_in(request):
    return render(request, "sign_in.html", RequestContext(request))

def categorize(request):
    return render(request, "categorize.html")

@login_required
def inbox(request, provider_id):
    name_style="inbox"
    contacts = request.user.contact_set.all()
    selected = provider_id and contacts.get(provider_id=provider_id) or contacts.all()[0]
    messages = request.user.milibox_set.all()[0].messages.order_by('-id')
    return render(request, "inbox.html", locals())

@login_required
def compose(request, provider_id):
    name_style="compose"
    contacts = request.user.contact_set
    selected = provider_id and contacts.get(provider_id=provider_id) or contacts.all()[0]
    contacts = contacts.all()
    return render(request, "compose.html", locals())

def attachments(request, provider_id):
    name_style="attachments"
    contacts = request.user.contact_set.all()
    selected = provider_id and contacts.get(provider_id=provider_id) or contacts.all()[0]
    return render(request, "attachments.html")


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
        mail_box = MiliBox.objects.get(user=request.user)
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
    mail_box=MiliBox.objects.create(name="MiliBox", user=request.user)
    return HttpResponseRedirect("/")

