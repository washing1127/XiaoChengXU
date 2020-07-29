from django.db import models


# Create your models here.
class daily_question(models.Model):
    def __str__(self):
        return str(self.date)
    name = models.CharField(max_length=30)
    data = models.TextField()
    date = models.CharField(max_length=30)
