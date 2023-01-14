from django.db import models
from common.models import CommonModel

class Photo(CommonModel):
    
    file = models.ImageField(blank=True,)
    descriptions = models.CharField(max_length=140,)
    room = models.ForeignKey("rooms.Room",on_delete=models.CASCADE,null=True,blank=True)
    experience = models.ForeignKey("experiences.Experience",on_delete=models.CASCADE, null=True,blank=True)
    
class Video(CommonModel):
        
    file=models.FileField(blank=True,)
    experience = models.OneToOneField("experiences.Experience",on_delete=models.CASCADE,blank=True,)
