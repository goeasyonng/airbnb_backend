from django.db import models
from common.models import CommonModel

class ChattingRoom(CommonModel):
    """Doom Model Definition"""
    
    users = models.ManyToManyField("users.User")
    
class Message(CommonModel):
    """Message Model Definition"""
    
    text = models.TextField()
    user = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL)
    room = models.ForeignKey("directmessage.ChattingRoom", on_delete=models.CASCADE)