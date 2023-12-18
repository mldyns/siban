from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = (
  ('Superadmin', 'superadmin'),
  ('Admin', 'admin'),
  ('TKSK', 'tksk')
)
class User(AbstractUser):
  is_superadmin = models.BooleanField('Is Superadmin', default=False)
  is_admin = models.BooleanField('Is Admin', default=False)
  is_tksk = models.BooleanField('Is TKSK', default=False)
  role = models.CharField(max_length=20, choices=ROLE, default=2)
  name = models.CharField(max_length=250)
  location = models.CharField(max_length=50, null=True)

  def __str__(self):
    return "{}".format(self.name)