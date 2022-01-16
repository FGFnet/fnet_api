from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.fields import BooleanField
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

class AdminType(object):
    REGULAR_USER = "Regular User"
    ADMIN = "Admin"

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, name, student_id):
        try:
            fg = self.model(
                name = name, student_id = student_id
            )
            fg.set_password(student_id)
            fg.save(using=self._db)
            return fg
        except Exception as e:
            print(e)
    def create_superuser(self, name, password, student_id="root"):
        try:
            fg = self.create_user(
                name=name, 
                student_id = password if password else student_id
            )
            fg.is_admin = True
            fg.save(using=self._db)
            return fg
        except Exception as e:
            print(e)


class FG(AbstractBaseUser):
    name = models.CharField(max_length=30, unique=True)
    student_id = models.CharField(max_length=10, validators=[MinLengthValidator(10)], null=True)
    is_admin = models.BooleanField(default=False) # True = 운영진, False = 활동기수
    is_active = models.BooleanField(default=True)
    campus = models.CharField(max_length=10, default="n")

    objects = UserManager()
    
    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'fg'
        ordering = ['is_admin', 'student_id']