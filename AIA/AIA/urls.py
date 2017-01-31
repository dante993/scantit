"""AIA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib import admin
from scanm.views import *


urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    url(r'^$', loginView, name='login'),
    url(r'^logout/$', logoutView, name='logout'),
    url(r'^inicio/$', v_inicio, name='inicio'),
    url(r'^area_imagen/$', v_cargar_img, name='area_img'),
    url(r'^crear_historial_clinico/$', Historial_clinicoCreate, name='crear_historial_clinico'),
    url(r'^cargar_imagen/$', ImagenCreate, name='crear_imagen'),

    # url(r'^login/$', auth_views.login, name='login'),
    # url(r'^cerrar/$', auth_views.logout, name='logout'),
    # url(r'^cerrar/$','django.contrib.auth.views.logout_then_login',name='logout'),
]
