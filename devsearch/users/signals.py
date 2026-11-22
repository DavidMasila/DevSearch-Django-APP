from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def createProfile(instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            username = instance.username,
            email = instance.email,
            name = instance.first_name
        )

        subject = 'Welcome to DevSearch'
        message = 'We are glad you are here!'
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )


@receiver(post_delete, sender=Profile)
def deleteUser(instance, **kwargs):
    instance.user.delete()

@receiver(post_save, sender=Profile)
def updateUser(instance, created, **kwargs):
    user = instance.user
    if created == False:
        user.first_name = instance.name
        user.username = instance.username
        user.email = instance.email
        user.save()