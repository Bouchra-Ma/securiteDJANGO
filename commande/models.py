import uuid
from django.db import models



class Product(models.Model):
    reference = models.CharField(max_length=50, unique=True, default=uuid.uuid4, editable=False)  
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)  
    quantite = models.PositiveIntegerField()  

    def __str__(self):
        return f"{self.nom} ({self.reference})"
    
