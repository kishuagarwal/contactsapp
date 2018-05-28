from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    # Only allow unique email address for each contact
    email_address = models.EmailField(unique=True, db_index=True)
    number = models.CharField(max_length=15, db_index=True)

