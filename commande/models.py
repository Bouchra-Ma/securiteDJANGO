import uuid
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    reference = models.CharField(max_length=50, unique=True, default=uuid.uuid4, editable=False)  
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)  
    quantite = models.PositiveIntegerField()  
    image = models.ImageField(upload_to='Bouchra/', null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.reference})"
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier de {self.user.username if self.user else 'Anonyme'}"

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    def subtotal(self):
        return self.product.price * self.quantity


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    lu = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.user.email} - {self.lu}"

class StockAlert(models.Model):
    email = models.EmailField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    notified = models.BooleanField(default=False)  # pour savoir si le mail a été envoyé
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} -> {self.product.nom}"