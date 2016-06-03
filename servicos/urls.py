from django.conf.urls import include, url

from servicos.views import SistemaCrud, SolicitacaoCrud

from .apps import AppConfig

app_name = AppConfig.name

urlpatterns = [
    url(r'sistema/', include(SistemaCrud.get_urls())),
    url(r'ticket/', include(SolicitacaoCrud.get_urls())),
]
