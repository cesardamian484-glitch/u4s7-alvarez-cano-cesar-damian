"""
URL configuration for miproyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# admin: ya viene importado por defecto, no lo borres
from django.contrib import admin
# path, include: include permite delegar un grupo de rutas a otra app
from django.urls import path, include

urlpatterns = [
    # ruta del panel de administración, ya incluida por defecto
    path('admin/', admin.site.urls),
    # '': todo lo que llegue a la raíz del sitio se delega a core/urls.py
    path('', include('core.urls')),
]
