from django.shortcuts import render, redirect, get_object_or_404
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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from .tasks import send_product_notification
from .models import Notification
from django.views.decorators.csrf import csrf_exempt





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

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def api_products(request):
#     produits = Product.objects.all().values("reference","nom","prix","quantite")
#     return Response(list(produits))

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
# Ajout au panier
def cart_detail(request):
    cart = request.session.get("cart", {})

    # Calculer le total et ajouter le total par produit
    total_price = 0
    for item in cart.values():
        # Vérifie que l'item est bien un dict et contient les bonnes clés
        if isinstance(item, dict) and 'quantity' in item and 'prix' in item:
            item['total_price'] = item['quantity'] * item['prix']
            total_price += item['total_price']
        else:
            # Si l'item est mal formé, on ignore ou on le convertit
            item = {'quantity': int(item), 'prix': 0, 'total_price': 0}

    return render(request, "commande/cart_detail.html", {"cart": cart, "total_price": total_price})




def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)]["quantity"] += 1
    else:
        cart[str(product_id)] = {
            "product_name": product.nom,
            "prix": float(product.prix),
            "quantity": 1
        }

    request.session["cart"] = cart
    return redirect("cart_detail")

    

def cart_remove(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session["cart"] = cart
    return redirect("cart_detail")


    class ProductPagination(PageNumberPagination):
       page_size = 3  # nombre de produits par page
       page_size_query_param = 'page_size'
       max_page_size = 10




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_products(request):
    produits = Product.objects.all()
    paginator = ProductPagination()
    result_page = paginator.paginate_queryset(produits, request)
    serializer = ProductSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)




 

# API pour récupérer les notifications de l'utilisateur
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-id')
    data = [
        {
            "id": n.id,
            "message": n.message,
            "lu": n.lu,
            "created_at": n.created_at
        } 
        for n in notifications
    ]
    return Response(data)



@csrf_exempt
def subscribe_stock_alert(request, product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        product = Product.objects.get(id=product_id)
        alert, created = StockAlert.objects.get_or_create(email=email, product=product)
        return JsonResponse({'success': True, 'message': 'Vous serez notifié lorsque le produit sera en stock !'})


def update_product_stock(request, product_id):
    from .tasks import send_stock_alert  # import local pour éviter circular import
    product = Product.objects.get(id=product_id)
    product.quantite += 1
    product.save()
    send_stock_alert.delay(product.id)
    return HttpResponse(f"Stock de {product.nom} mis à jour et notifications envoyées !")
