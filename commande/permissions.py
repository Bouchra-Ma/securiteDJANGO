from rest_framework import permissions

class CanBuyExpensiveProduct(permissions.BasePermission):
    """
    Autorise seulement les utilisateurs qui peuvent acheter des produits <= 1000€.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.prix <= 1000