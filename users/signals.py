from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
      
        instance.generate_activation_code()
        instance.save(update_fields=['activation_code'])
        
        send_mail(
            subject="Код активации",
            message=f"Ваш код активации: {instance.activation_code}",
            from_email="no-reply@example.com",
            recipient_list=[instance.email],
        )
