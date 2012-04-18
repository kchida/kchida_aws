from django.contrib.auth.models import User
from django.db import models


class MyUser(User):

    #TODO: add profile one-to-one
    is_registered = models.BooleanField()
