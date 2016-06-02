from django.conf.urls import include, url
from django.contrib.auth.views import login, logout

from usuarios.forms import LoginForm
from usuarios.views import UsuarioCrud, HabilitarDetailView, HabilitarEditView

from .apps import AppConfig

app_name = AppConfig.name

urlpatterns = [
    url(r'^login/$', login, {
        'template_name': 'usuarios/login.html',
        'authentication_form': LoginForm},
        name='login'),
    url(r'^logout/$', logout, {'next_page': '/login'}, name='logout'),
    url(r'^usuario/', include(UsuarioCrud.get_urls())),
    url(r'^habilitar/(?P<pk>\d+)$',
        HabilitarDetailView.as_view(), name='habilitar_detail'),
    url(r'^habilitar/(?P<pk>\d+)/edit$',
        HabilitarEditView.as_view(), name='habilitar_edit'),
]
