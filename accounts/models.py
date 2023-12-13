from audioop import reverse
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, Group, Permission



class Profile(models.Model):
    user=models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE)
    friend=models.ManyToManyField('Friend',related_name='user_friends')
    friend_request=models.ManyToManyField('Friend',related_name='user_friend_requests')
    phone=models.CharField(max_length=20,verbose_name=_("phone"))
    slug=models.SlugField(blank=True, null=True) 
    image=models.ImageField(upload_to='profile/',blank=True, null=True)
    country=CountryField(blank_label='select country')
    adress=models.CharField(max_length=100)
    Token=models.CharField(max_length=500,blank=True, null=True)
    join_date=models.DateTimeField(verbose_name=_("Created At"), default=datetime.now)
    
    def save(self ,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return '%s' %(self.user)

    def get_absolute_url(self):
        return reverse("accounts:Profile_detail", kwargs={"slug": self.slug})

    def create_profile(sender ,*args, **kwargs):
        if kwargs['created']:
            user_profile=Profile.objects.create(user=kwargs['instance'])    
    post_save.connect(create_profile , sender=User)

class Friend(models.Model):
    profile=models.OneToOneField(Profile, verbose_name=_("user"), on_delete=models.CASCADE,related_name='friend_profile')
    

    class Meta:
        verbose_name = _("Friend")
        verbose_name_plural = _("Friends")

    def __str__(self):
        return str(self.profile)

    def get_absolute_url(self):
        return reverse("Friend_detail", kwargs={"pk": self.pk})
    @staticmethod
    def create_friend(sender, instance, created, **kwargs):
        if created:
            profile_instance = Profile.objects.get(user=instance)
            Friend.objects.create(profile=profile_instance)
post_save.connect(Friend.create_friend, sender=User)