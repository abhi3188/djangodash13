from oauth2client.django_orm import Storage

from mails.models import Credential

def get_user_credential(user):
    storage = Storage(Credential, 'id', user.id, 'credential')
    return storage.get()
