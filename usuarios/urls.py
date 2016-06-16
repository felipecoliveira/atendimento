from django.conf.urls import include, url
from django.contrib.auth.views import (login, logout, password_reset,
                                       password_reset_done,
                                       password_reset_confirm,
                                       password_reset_complete)
from atendimento.settings import EMAIL_SEND_USER
from usuarios.forms import (LoginForm, RecuperarSenhaEmailForm,
                            RecuperacaoMudarSenhaForm)
from usuarios.views import (HabilitarDetailView, HabilitarEditView,
                            MudarSenhaView, UsuarioCrud, ConfirmarEmailView)

from .apps import AppConfig

app_name = AppConfig.name

recuperar_email = [
    url(r'^recuperar/recuperar_senha/$',
        password_reset,
        {'template_name': 'usuarios/recuperar_senha.html',
         'password_reset_form': RecuperarSenhaEmailForm,
         'post_reset_redirect': 'usuarios:recuperar_senha_finalizado',
         'email_template_name': 'usuarios/recuperar_senha_email.html',
         'from_email': EMAIL_SEND_USER,
         'html_email_template_name': 'usuarios/recuperar_senha_email.html'},
        name='recuperar_senha'),
    url(r'^recuperar/recuperar_recuperar/finalizado/$',
        password_reset_done,
        {'template_name': 'usuarios/recuperar_senha_enviado.html'},
        name='recuperar_senha_finalizado'),
    url(r'^recuperar/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        password_reset_confirm,
        {'post_reset_redirect': 'usuarios:recuperar_senha_completo',
         'template_name': 'usuarios/recuperacao_senha_form.html',
         'set_password_form': RecuperacaoMudarSenhaForm},
        name='recuperar_senha_confirma'),
    url(r'^recuperar/completo/$',
        password_reset_complete,
        {'template_name': 'usuarios/recuperacao_senha_completo.html'},
        name='recuperar_senha_completo'),
]

urlpatterns = recuperar_email + [
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
    url(r'^usuario/confirmar/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        ConfirmarEmailView.as_view(), name='confirmar_email'),
]
