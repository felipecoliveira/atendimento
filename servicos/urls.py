from django.conf.urls import include, url

from servicos.views import TicketCrud, SistemaCrud

urlpatterns = [
    url(r'', include(SistemaCrud.get_urls())),
    url(r'', include(TicketCrud.get_urls())),
]
