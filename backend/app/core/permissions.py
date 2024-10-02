from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core.models import Session, Role



def HasRole(role_list):
    class HasRole(BasePermission):
        roles = role_list

        def __innit__(self):
            super().__init__
            self.roles = role_list

        def has_permission(self, request, view):
            user = request.user 
            return user.role in self.roles
    

class IsLogged(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        res = Session.is_logged(user) or user.is_superuser
        return bool(res)


