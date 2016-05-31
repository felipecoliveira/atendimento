from django.conf.urls import include, url
from usuarios.views import UsuarioExternoCrud

from .apps import AppConfig

app_name = AppConfig.name

urlpatterns = [
    url(r'^login/$', login, {
        'template_name': 'usuarios/login.html',
        'authentication_form': LoginForm},
        name='login'),
    url(r'^logout/$', logout, {'next_page': '/login'}, name='logout')
    url(r'^usuario-externo/', include(UsuarioExternoCrud.get_urls())),
]
