# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.template import RequestContext

from contacts.models import Contact,ContactEmail

def all_contacts(request):
	contacts = Contact.objects.filter(user=request.user)
	return render (request,"contacts.html",locals())