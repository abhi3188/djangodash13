from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

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

    def display_name(self):
        return self.name or self.contactemail_set.all()[0]


class ContactEmail(models.Model):
    contact = models.ForeignKey(Contact)
    email = models.EmailField()

    def __unicode__(self):
        return self.email


