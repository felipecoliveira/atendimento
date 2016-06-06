import crud.base
from crud.base import Crud

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from .forms import SistemaForm, TicketForm
from .models import Sistema, Ticket

from usuarios.models import Usuario


class TicketCrud(Crud):
    model = Ticket
    help_path = ''

    class CreateView(PermissionRequiredMixin, crud.base.CrudCreateView):
        form_class = TicketForm
        permission_required = {'usuarios.add_ticket'}

        def get_initial(self):
            # Essa query no caso de super_user é só para nao quebrar
            if self.request.user.is_superuser:
                return {'usuario': Usuario.objects.all()[0]}
            else:
                return {'usuario': Usuario.objects.get(
                    user=self.request.user.id)}

    class UpdateView(crud.base.CrudUpdateView):
        form_class = TicketForm
        permission_required = {'usuarios.change_ticket'}

        def get_initial(self):
            # Essa query no caso de super_user é só para nao quebrar,
            # Deverá ser retirada no futuro
            if self.request.user.is_superuser:
                return {'usuario': Usuario.objects.all()[0]}
            else:
                return {'usuario': Usuario.objects.get(
                    user=self.request.user.id)}

    class ListView(LoginRequiredMixin, crud.base.CrudListView):

        def get_queryset(self):
            if self.request.user.groups.filter(name='Usuário Comum'):
                queryset = Ticket.objects.filter(
                    usuario__user=self.request.user.id)
            else:
                queryset = Ticket.objects.all()

            return queryset


class SistemaCrud(Crud):
    model = Sistema
    help_path = ''

    class CreateView(crud.base.CrudCreateView):
        form_class = SistemaForm

    class UpdateView(crud.base.CrudUpdateView):
        form_class = SistemaForm
