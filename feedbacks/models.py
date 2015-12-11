from django.db import models

# Create your models here.

class Feedback(models.Model):
    name = models.CharField(max_length = 100)
    subject = models.CharField(max_length = 255)
    message = models.TextField()
    from_email = models.EmailField()
    create_date = models.DateTimeField(auto_now_add=True)
