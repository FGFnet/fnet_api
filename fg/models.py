from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.fields import BooleanField

# Create your models here.
class FG(models.Model):
    name = models.CharField(max_length=30)
    student_id = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    admin = BooleanField(default=False) # True = 운영진, False = 활동기수