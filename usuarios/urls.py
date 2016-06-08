from django.conf.urls import include, url
from django.contrib.auth.views import (login, logout, password_reset,
                                       password_reset_done,
                                       password_reset_confirm,
                                       password_reset_complete)

from usuarios.forms import LoginForm, RecuperarSenhaForm
from usuarios.views import (HabilitarDetailView, HabilitarEditView,
                            MudarSenhaView, UsuarioCrud)

from .apps import AppConfig

app_name = AppConfig.name

urlpatterns = [
    url(r'^recuperar/recuperar_senha/$',
        password_reset,
        {'template_name': 'usuarios/recuperar_senha.html',
         'password_reset_form': RecuperarSenhaForm,
         'post_reset_redirect': 'usuarios:recuperar_senha_finalizado'},
        name='recuperar_senha'),
    url(r'^recuperar/recuperar_recuperar/finalizado/$',
        password_reset_done,
        name='recuperar_senha_finalizado'),
    url(r'^recuperar/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        password_reset_confirm,
        name='recuperar_senha_confirma'),
    url(r'^recuperar/completo/$',
        password_reset_complete,
        name='recuperar_senha_completo'),
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
    url(r'^usuario/(?P<pk>\d+)/mudar_senha$',
        MudarSenhaView.as_view(), name='mudar_senha'),

]
