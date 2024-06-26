from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import OtpToken
from django.core.mail import send_mail
from django.utils import timezone


@receiver(post_save, sender=settings.AUTH_USER_MODEL) 
def create_token(sender, instance, created, **kwargs):
    print("Inside create_token function")
    if created:
        print("New user created")
        if instance.is_superuser:
            print("User is a superuser")
            pass
        else:
            print("User is not a superuser")
            otp = OtpToken.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            instance.is_active = False 
            instance.save()

            subject = "Email Verification"
            message = f"""
                        Hi {instance.username}, here is your OTP {otp.otp_code} 
                        it expires in 5 minute, use the url below to redirect back to the website
                        http://127.0.0.1:8000/verify-email/{instance.username}

                        """
            sender = "premkumransathya@gmail.com"
            receiver = [instance.email, ]

            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )

            print("Email sent with OTP")

