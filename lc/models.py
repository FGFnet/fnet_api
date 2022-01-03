from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateField, IntegerField
from django.db.models.fields.related import ForeignKey
from fg.models import FG

# Create your models here.
class LC(models.Model):
    fg = ForeignKey(FG, on_delete=CASCADE)
    name = CharField(max_length=10)
    total = IntegerField()
    schedule = DateField(null=True)

    class Meta:
        db_table = 'lc'
        ordering = ['name']