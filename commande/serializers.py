from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()  # Pour générer l'URL complète

    class Meta:
        model = Product
        fields = ['id', 'reference', 'nom', 'prix', 'quantite', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return obj.image.url 
        return None

    def update(self, instance, validated_data):
        # Simuler l'achat en décrémentant la quantité
        if 'quantite' in validated_data:
            instance.quantite += validated_data['quantite']  # -1 pour décrémenter
            if instance.quantite < 0:
                raise serializers.ValidationError("Stock insuffisant.")
            instance.save()
        return instance

        