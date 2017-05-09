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
# from django.conf import settings
# from django.views.static import serve

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    url(r'^$', loginView, name='login'),
    url(r'^logout/$', logoutView, name='logout'),
    url(r'^inicio/$', v_inicio, name='inicio'),
    url(r'^registro/$', UsuaioC, name='registro'),

    # ------------------------------Historial_clinico-----------------------------------
    url(r'^historial_clinico/$', Historial_clinicoList, name='historial_clinico'),
    url(r'^historial_clinico/inactivos/$', Historial_clinicoListin, name='historial_clinicoin'),
    url(r'^historial_clinico/crear_historial_clinico/$', Historial_clinicoCreate, name='crear_historial_clinico'),
    url(r'^historial_clinico/editar/(?P<pk>.*)/$', Historial_clinicoUpdate, name='editar_historial_clinico'),
    url(r'^historial_clinico/borrar/(?P<pk>.*)/$', Historial_clinicoDelete, name='borrar_historial_clinico'),
    url(r'^historial_clinico/borrar_permanente/(?P<pk>.*)/$', Historial_clinicoDeleteP, name='borrar_p_historial_clinico'),
    url(r'^historial_clinico/restaurar/(?P<pk>.*)/$', Historial_clinicoRestore, name='restaurar_historial_clinico'),

    # ------------------------------imagen-----------------------------------
    url(r'^imagen/$', ImagenList, name='imagen'),
    # url(r'^imagen/inactivos/$', Historial_clinicoListin, name='historial_clinicoin'),evaluar_imagen
    url(r'^imagen/crear_imagen/$', ImagenCreate, name='crear_imagen'),
    url(r'^imagen/editar/(?P<pk>.*)/$', ImagenUpdate, name='editar_imagen'),
    url(r'^imagen/borrar/(?P<pk>.*)/$', ImagenDelete, name='borrar_imagen'),
    url(r'^imagen/evaluar_imagen/(?P<pk>.*)/$', ImagenEvaluate, name='evaluar_imagen'),

    url(r'^area_imagen/$', v_area_img, name='area_img'),

    # url(r'^login/$', auth_views.login, name='login'),
    # url(r'^cerrar/$', auth_views.logout, name='logout'),
    # url(r'^cerrar/$','django.contrib.auth.views.logout_then_login',name='logout'),

# -----------------------------------------------admin-----------------------------------------------------
    url(r'^admin/imagen/$', Imagen_admList, name='adm_imagen'),
    url(r'^admin/imagen/crear/(?P<pk>.*)/(?P<pk2>.*)/$', Imagen_admCreate, name='crear_adm_imagen'),
    url(r'^admin/imagen/retrain/$', Imagen_admRetrain, name='retrain_adm_imagen'),
    url(r'^admin/imagen/evaluate/$', Imagen_admEvaluate, name='evaluate_adm_imagen'),

    # ------------------------------tipos de cancer-----------------------------------
    url(r'^admin/tipo_de_cancer/$', Tipo_cancerList, name='tipo_cancer'),
    url(r'^admin/tipo_de_cancer/inactivos/$', Tipo_cancerListin, name='tipo_cancer_in'),
    url(r'^admin/tipo_de_cancer/crear/$', Tipo_cancerCreate, name='crear_tipo_cancer'),
    url(r'^admin/tipo_de_cancer/crear/$', Tipo_cancerCreate, name='crear_tipo_cancer'),
    url(r'^admin/tipo_de_cancer/editar/(?P<pk>.*)/$', Tipo_cancerUpdate, name='editar_tipo_cancer'),
    url(r'^admin/tipo_de_cancer/borrar/(?P<pk>.*)/$', Tipo_cancerDelete, name='borrar_tipo_cancer'),
    url(r'^admin/tipo_de_cancer/borrar_permanente/(?P<pk>.*)/$', Tipo_cancerDeleteP, name='borrar_p_tipo_cancer'),
    url(r'^admin/tipo_de_cancer/restaurar/(?P<pk>.*)/$', Tipo_cancerRestore, name='restaurar_tipo_cancer'),

]


# if settings.DEBUG:
#     urlpatterns += [
#         url(r'^media/(?P<path>.*)$', serve, {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#     ]
