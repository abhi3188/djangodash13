from django.db import models
from django.contrib.auth.models import User


from oauth2client.django_orm import CredentialsField

class Credential(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()



