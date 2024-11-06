from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from db.models import Permissions, CustomUser

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_permissions(sender, instance, created, **kwargs):
    if created:
        admin_exists = CustomUser.objects.filter(product_owner=True).exists()
        if not admin_exists:
            instance.product_owner = True
            instance.is_staff = False
            instance.is_superuser = False
            instance.save()  # Speichere die Änderung

            # Erster Benutzer wird Admin mit allen Rechten
            Permissions.objects.create(
                user=instance,
                can_add_customuser=True,
                can_edit_customuser=True,
                can_delete_customuser=True,
                can_add_object=True,
                can_edit_object=True,
                can_delete_object=True,
                can_add_schedule=True,
                can_edit_schedule=True,
                can_delete_schedule=True
            )
        else:
            # Weitere Benutzer erhalten Standardberechtigungen
            Permissions.objects.create(user=instance)
