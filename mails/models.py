import imaplib
import email

from django.db import models
from django.contrib.auth.models import User

from django_mailbox.models import Mailbox
from oauth2client.django_orm import CredentialsField, Storage

class GmailTransport(object):

    def connect(self, user):
        ''' connect using gmails XOAUTH authentication '''
        credential = user.credential_set.all()[0]
        if not user or not credential: # also if user does not have credentials
            return None
        self.server = imaplib.IMAP4_SSL('imap.googlemail.com')
        print 'user=%s\1auth=Bearer %s\1\1' % (user.email, credential.credential.access_token)
        self.server.authenticate('XOAUTH2',
                          lambda x : 'user=%s\1auth=Bearer %s\1\1' % (user.email, credential.credential.access_token))
        self.server.select()

    def get_message(self):
        ''' get messages without deleting on server.'''
        typ, inbox = self.server.search(None, 'All')
        if inbox[0]:
            for key in inbox[0].split():
                try:
                    typ, msg_contents = self.server.fetch(key, '(RFC822)')
                    message = email.message_from_string(msg_contents[0][1])
                    yield message
                except email.Errors.MessageParseError:
                        continue


class CredentialManager(models.Manager):

    def get_for_user(self, user):
        storage = Storage(Credential, 'id', user, 'credential')
        return storage.get()


class Credential(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()
    objects = CredentialManager()

class MiliBox(Mailbox):
    user = models.ForeignKey(User)

    def get_connection(self):
        conn = GmailTransport()
        conn.connect(self.user)
        return conn
