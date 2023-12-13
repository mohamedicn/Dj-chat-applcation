from django.db import models
from accounts.models import Profile
# Create your models here.
from datetime import datetime
from django.utils.translation import gettext_lazy as _
class ChatMessage(models.Model):
    body = models.TextField()
    msg_sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='msg_sender')
    msg_receiver = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='msg_receiver')
    seen=models.BooleanField(default=False)
    send_in = models.DateTimeField(verbose_name=_("Time Send"), default=datetime.now)

    def __str__(self):
        return self.body

    def __unicode__(self):
        return 
