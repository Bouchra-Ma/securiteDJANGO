from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Product
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import CanBuyExpensiveProduct
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponseForbidden
from django.http import HttpResponse

# Décorateur personnalisé pour JWT
def jwt_auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            auth = JWTAuthentication()
            header = request.META.get('HTTP_AUTHORIZATION')
            if header:
                raw_token = header.split(' ')[1]  # Extrait "Bearer <token>"
                validated_token = auth.get_validated_token(raw_token)
                user = auth.get_user(validated_token)
                request.user = user
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("Token manquant")
        except AuthenticationFailed:
            return HttpResponseForbidden("Token invalide")
    return wrapper

# Vues JWT
def home_jwt_view(request):
    return render(request, 'commande/index.html')

def login_jwt_view(request):
    return render(request, 'commande/login.html')

def form(request):
    return render(request, 'commande/form.html')

def dashboard(request):
    return render(request, 'commande/dashboard.html')


def products(request):
    produits = Product.objects.all()
    return render(request, "commande/products.html", {"produits": produits})

@jwt_auth_required
def buy_product(request, product_id):
    if request.method != "POST":
        return HttpResponseForbidden("Méthode non autorisée")

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseForbidden("Produit non trouvé.")

    # Vérifier la permission
    permission = CanBuyExpensiveProduct()
    if not permission.has_object_permission(request, None, product):
        return HttpResponseForbidden(f"Vous ne pouvez pas acheter {product.nom} (prix : {product.prix}€, limite : 1000€).")

    if product.quantite > 0:
        product.quantite -= 1
        product.save()  # Assurez-vous que cette ligne enregistre en base
        return HttpResponse(f"Achat de {product.nom} effectué avec succès !")
    else:
        return HttpResponse(f"Le produit {product.nom} est en rupture de stock.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_dashboard(request):
    return Response({"username": request.user.username, "stats": {...}})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_products(request):
    produits = Product.objects.all().values("reference","nom","prix","quantite")
    return Response(list(produits))

# Inscription compatible JWT
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion temporaire pour compatibilité
            return redirect('home_jwt')
    else:
        form = UserCreationForm()
    return render(request, 'commande/login.html', {'form': form})

# Déconnexion adaptée pour JWT
def logout_view(request):
    # Pour JWT, on ne supprime pas la session côté serveur
    messages.success(request, "Déconnexion réussie !")
    return redirect('home_jwt')

# --------------------------------------
# Vues classiques Django (auth par session)

# --------------------------------------

# def home(request): 
#     return render(request, 'commande/index.html')

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return render(request, 'commande/form.html')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'commande/login.html', {'form': form})
