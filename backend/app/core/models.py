"""
Database models
"""
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
import django.contrib.auth as DjangoAuth
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)

from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework.permissions import BasePermission


class Role(models.Model):
    """User roles in the system"""

    ADMIN = 'Administrador'
    TEACHER = 'Profesor'
    STUDENT = 'Estudiante'
    PARENT = 'Padre'

    role_name = models.CharField(max_length=255, unique=True, primary_key=True)

    @classmethod
    def createAdminRole(cls):
        try:
            cls.objects.get(role_name = cls.ADMIN)
            print(cls.ADMIN + " already Added")
        except:
            cls.objects.create(role_name = cls.ADMIN)
            print(cls.ADMIN + " admin Added")

    @classmethod
    def createTeacherRole(cls):
        try:
            cls.objects.get(role_name = cls.TEACHER)
            print(cls.TEACHER + " already Added")
        except:
            cls.objects.create(role_name = cls.TEACHER)
            print(cls.TEACHER + " admin Added")

    @classmethod
    def createParentRole(cls):
        try:
            cls.objects.get(role_name = cls.PARENT)
            print(cls.PARENT + " already Added")
        except: 
            cls.objects.create(role_name = cls.PARENT)
            print(cls.PARENT + " admin Added")

    @classmethod
    def createStudentRole(cls):
        try:
            cls.objects.get(role_name = cls.STUDENT)
            print(cls.STUDENT + " already Added")
        except:
            cls.objects.create(role_name = cls.STUDENT)
            print(cls.STUDENT + " added")

    @classmethod
    def createRoles(cls):
        cls.createAdminRole()
        cls.createParentRole()
        cls.createTeacherRole()
        cls.createStudentRole()

    @classmethod
    def get_admin(cls):
        try:
            return cls.objects.get(role_name=cls.ADMIN) 
        except:
            return None 
    
    @classmethod
    def get_role(cls):
        try:    
            return cls.objects.get(role_name=cls.PARENT)
        except:
            return None
    
    @classmethod
    def get_teacher(cls):
        try:
            return cls.objects.get(role_name=cls.TEACHER)
        except:
            return None
    
    @classmethod
    def get_student(cls):
        try:
            return cls.objects.get(role_name=cls.STUDENT)
        except:
            return None



class UserManager(BaseUserManager):
    """Manager for users."""

    def generate_email(self, names, last_names, extension, **extra_fields):
        names = names.split(' ')
        last_names = last_names.split(' ')
        if(len(names)<1 or len(last_names)<1):
            raise ValueError('Nombre inválido')
        
        for namex in names:
            if not namex.isalpha():
                raise ValueError(f'El nombre {namex} inválido')
        for namex in last_names:
            if not namex.isalpha():
                raise ValueError(f'El apellido {namex} es inválido')

        names_str = names[0]
        last_names_str = last_names[0]

        names = '.' + '.'.join(names[1:]) if len(names)>1 else ''
        last_names = '.' + '.'.join(last_names[1:]) if len(last_names)>1 else ''

        new_email = f'{names_str}.{last_names_str}@{extension}.com'
        query = self.filter(email=new_email)
        i=0
        j=0
        c=1
        while(query.exists()):
            if(len(last_names_str)>j):    
                    last_names_str += last_names[j]
                    if(last_names[j]=='.'):
                        j += 1
                        last_names_str += last_names[j]
            else:
                if(len(names_str)>i):
                    names_str += names[i]
                    if(names[i]=='.'):
                        i += 1
                        names_str += names[i]
                else:
                    last_names_str += str(c)
                    c += 1   
            new_email = f'{names_str}.{last_names_str}@{extension}.com'
            query = self.filter(email=new_email)
     
    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, role=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        validate_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, email, password=None, **extra_fields):
        role = Role.getAdminRole()
        return self.create_user(email, password, role, **extra_fields)

    def create_teacher(self, first_name, last_name, password=None, **extra_fields):
        role = Role.getTeacherRole()
        email = self.generate_email(first_name, last_name)
        return self.create_user(email, password, role, **extra_fields)
        

    def create_parent(self, first_name, last_name, password=None, **extra_fields):
        role = Role.getParentRole()
        email = self.generate_email(first_name, last_name)
        return self.create_user(email, password, role, **extra_fields)
        
    def create_student(self, first_name, last_name, password=None, **extra_fields):
        role = Role.getStudentRole()
        email = self.generate_email(first_name, last_name)
        return self.create_user(email, password, role, **extra_fields)
    
    @classmethod
    def createSuperInstance(cls):
        data = {
                'email' : 'admin@example.com',
                'password' : 'admin',
        }
        admin = get_user_model().objects.filter(email = data['email']).first()
        if admin:
            print("Admin instance already created")
            return

        get_user_model().objects.create_superuser(**data)
        print("Admin instance created")
        
        

class User(AbstractBaseUser):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.RESTRICT)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Session(models.Model):
    user = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time =  models.DateTimeField(null=True, blank=True)
    #session_key = models.CharField(max_length=255,  null=False, blank=True)

    @classmethod
    def get_last_session(self, user):
        if not user.is_authenticated: return None
        last_session = Session.objects.filter(user=user).order_by('-login_time').first()
        if last_session:
            return last_session
        else:
            return None

    @classmethod
    def get_open_session(self, user):
        last_session = self.get_last_session(user)
        if not last_session: return None
        if last_session.logout_time:
            return None
        else:
            return last_session

    @classmethod    
    def is_logged(self, user):
        if self.get_open_session(user) and user.is_authenticated:
            return True
        return False
    
    @classmethod
    def logout(self, user, request=None):
        if not user: user = request.user
        last_session = self.get_open_session(user)
        if not last_session:
            return
        last_session.logout_time = timezone.now()
        last_session.save()
        DjangoAuth.logout(user)

    @classmethod
    def login(self, user, request=None):
        if not user: user = request.user
        if not user.is_authenticated:
            return
        if self.get_open_session(user):
            self.logout(user)
        Session.objects.create(user=user)
        DjangoAuth.login(request, user)


