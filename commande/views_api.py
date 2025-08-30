from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import UserRateThrottle
from .models import Product
from .serializers import ProductSerializer
from .permissions import CanBuyExpensiveProduct

# Throttle perso (optionnel)
class ProductThrottle(UserRateThrottle):
    rate = '10/min'  # max 10 requêtes par minute par utilisateur

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]  # seul l’admin peut CRUD
    throttle_classes = [ProductThrottle]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CanBuyExpensiveProduct]  # permission personnalisée