from django.conf.urls import include, url

from servicos.views import SistemaCrud, TicketCrud

from .apps import AppConfig

app_name = AppConfig.name

urlpatterns = [
    url(r'sistema/', include(SistemaCrud.get_urls())),
    url(r'ticket/', include(TicketCrud.get_urls())),
]
