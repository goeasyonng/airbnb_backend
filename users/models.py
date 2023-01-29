from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")
    
    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")
    
    class CurrenyChoices(models.TextChoices):
        WON = ("won","Korean won")
        USD = ("usd","Dallar")
           
    first_name = models.CharField(max_length=150, editable = False)
    last_name = models.CharField(max_length=150, editable = False)
    avatar = models.ImageField(blank=True)
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices,)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices, )
    curreny = models.CharField(max_length=5, choices=CurrenyChoices.choices,)
    
    

