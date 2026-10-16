from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Ensure you import your custom User model

admin.site.register(User, UserAdmin)
