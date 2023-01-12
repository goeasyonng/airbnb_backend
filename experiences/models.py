from django.db import models
from common.models import CommonModel

class Experience(CommonModel):
    """Experiences Model Definition"""
    
    country = models.CharField(max_length=50, default="한국",)
    city = models.CharField(max_length=80, default="서울")
    name=models.CharField(max_length=250)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start_at=models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField("experiences.Perk",)
    
        
class Perk(CommonModel):
    
    """What is included on an Experience"""
        
    name=models.CharField(max_length=250,)
    details=models.CharField(max_length=250)
    explanation = models.TextField()
    