from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Coach(models.Model):
    user = models.OneToOneField(User)
    date_of_birth = models.DateField()
    gender_choices = ( ('M', 'Male'), ('F', 'Female') )
    gender = models.CharField(max_length = 1, choices = gender_choices, default='M')
    phone = models.CharField(max_length = 50)
    address = models.CharField(max_length = 255)
    skype = models.CharField(max_length = 255)
    description = models.TextField()

    def __unicode__(self):
	return self.user.username