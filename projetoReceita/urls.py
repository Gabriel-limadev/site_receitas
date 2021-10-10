from django.contrib import admin
from django.urls import path
from django.urls.conf import include
import receitas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('receitas.urls')),
]
