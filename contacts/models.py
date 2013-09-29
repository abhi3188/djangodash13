import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver

from django_mailbox.signals import message_received
from django_mailbox.models import Message
import gdata.gauth
import gdata.contacts.client

import utils

def get_contacts_for_user(user):
    credential = utils.get_user_credential(user)
    token = gdata.gauth.OAuth2Token(client_id=settings.CLIENT_SECRETS['client_id'],
        client_secret=settings.CLIENT_SECRETS['client_secret'],
        scope=settings.GOOGLE_SCOPE,
        user_agent='mily.testing',
        access_token=credential.access_token,
        refresh_token=credential.refresh_token)
    client = gdata.contacts.client.ContactsClient()
    token.authorize(client)
    feed = client.GetContacts()
    return feed.entry

class Contact(models.Model):

    CONTACT_TYPE = (
        (1,"family"),
        (2, "friends"),
        (3, "work"),
        (4, "others"),
    )
    user = models.ForeignKey(User)
    provider_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200,null=True,blank=True)
    image_link = models.CharField(max_length=250,null=True,blank=True)
    contact_type = models.IntegerField(choices = CONTACT_TYPE, default=4)
    system = models.BooleanField(default=False)

    def display_name(self):
        try:
            return self.name or self.contactemail_set.all()[0]
        except:
            return self.user    


class ContactEmail(models.Model):
    contact = models.ForeignKey(Contact)
    email = models.EmailField()

    def __unicode__(self):
        return self.email

class ContactMessage(models.Model):
    contact = models.ForeignKey(Contact)
    message = models.OneToOneField(Message)

@receiver(message_received)
def create_or_associate_contact(sender, message, **kwargs):
    sender_address = message.from_address[0]
    sender_query = ContactEmail.objects.filter(email=sender_address, contact__user=message.mailbox.milibox.user)
    if sender_query.exists():
        contact=sender_query.all()[0].contact
    else:
        contact = Contact.objects.create(user=message.mailbox.milibox.user, system=True, provider_id=uuid.uuid4())
        ContactEmail.objects.create(email=sender_address, contact=contact)
    ContactMessage.objects.create(message=message, contact=contact)


