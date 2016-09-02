"""diputados URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from website import views

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', views.Index, name='index'),
    url(r'^presentismo/$', views.Presentismo, name='presentismo'),

    #API
    url(r'^main/$', views.MainApi, name='main'),
    url(r'^diputado/$', views.DiputadosApi, name='diputados'),
    url(r'^diputado/(?P<id>[a-z]+)/$', views.DiputadoApi, name='diputado'),
    url(r'^diputado/(?P<id>[a-z]+)/proyectos/$', views.DiputadoProyectosApi, name='proyectos'),
    url(r'^proyecto/(?P<id>[0-9]+)/$', views.ProyectoApi, name='proyecto'),
    url(r'^diputado/(?P<id>[a-z]+)/comisiones/$', views.DiputadoComisionesApi, name='comisiones'),
    url(r'^asistencias/$', views.AsistenciasApi, name='asistencias'),
    url(r'^run/$', views.AsistenciasUpdate, name='run'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
