from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateField, IntegerField
from django.db.models.fields.related import ForeignKey
from fg.models import FG
from datetime import datetime

# Create your models here.
class LC(models.Model):
    fg_n = ForeignKey(FG, on_delete=CASCADE, null=True, related_name='fg_n')
    fg_s = ForeignKey(FG, on_delete=CASCADE, null=True, related_name='fg_s')
    name = CharField(max_length=10)
    schedule = DateField(default=datetime.now)
    class Meta:
        db_table = 'lc'
        ordering = ['schedule', 'name']