# commande/serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

def update(self, instance, validated_data):
        # Simuler l'achat en décrémentant la quantité
        if 'quantite' in validated_data:
            instance.quantite += validated_data['quantite']  # -1 pour décrémenter
            if instance.quantite < 0:
                raise serializers.ValidationError("Stock insuffisant.")
            instance.save()
        return instance
        