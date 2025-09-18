import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User, ActivationCode

@receiver(post_save, sender=User)
def create_activation_code(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        code = uuid.uuid4().hex
        ActivationCode.objects.update_or_create(user=instance, defaults={"code": code})
        subject = "Activation code"
        message = f"Hello {instance.email}\nYour activation code: {code}"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email])
