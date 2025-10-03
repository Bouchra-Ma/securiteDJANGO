from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Product, Notification
from django.conf import settings

@shared_task
def send_product_notification(product_id):
    try:
        product = Product.objects.get(id=product_id)
        users = User.objects.filter(is_active=True)
        for user in users:
            Notification.objects.create(
                user=user,
                message=f"Le produit {product.nom} est disponible en stock !"
            )
            send_mail(
                subject=f"Produit disponible : {product.nom}",
                message=f"Bonjour {user.username},\n\nLe produit {product.nom} est maintenant en stock.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
    except Product.DoesNotExist:
        pass
