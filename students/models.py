from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length = 100)
    surname = models.CharField(max_length = 100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length = 30)
    address = models.CharField(max_length = 255)
    skype = models.CharField(max_length = 255)
    courses = models.ManyToManyField('courses.Course')