from django.db import models
from django.conf import settings

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
