import crud.base
from crud.base import Crud

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from .forms import SistemaForm, SolicitacaoEditForm, SolicitacaoForm
from .models import Sistema, Solicitacao

from usuarios.models import Usuario


class SolicitacaoCrud(LoginRequiredMixin, Crud):
    model = Solicitacao
    help_path = ''

    class CreateView(PermissionRequiredMixin, crud.base.CrudCreateView):
        form_class = SolicitacaoForm
        permission_required = {'servicos.add_ticket'}

        def get_initial(self):
            # Essa query no caso de super_user é só para nao quebrar
            if self.request.user.is_superuser:
                return {'usuario': Usuario.objects.all()[0]}
            else:
                return {'usuario': Usuario.objects.get(
                    user=self.request.user.id)}

    class UpdateView(crud.base.CrudUpdateView):
        form_class = SolicitacaoEditForm
        permission_required = {'servicos.change_ticket'}

        @property
        def layout_key(self):
            return 'SolicitacaoEdit'

        def get_initial(self):
            # Essa query no caso de super_user é só para nao quebrar,
            # Deverá ser retirada no futuro
            if self.request.user.is_superuser:
                return {'usuario': Usuario.objects.all()[0]}
            else:
                return {'usuario': Usuario.objects.get(
                    user=self.request.user.id)}

    class ListView(LoginRequiredMixin, crud.base.CrudListView):
        @property
        def layout_key(self):
            return 'SolicitacaoList'

        def get_queryset(self):
            if self.request.user.groups.filter(name='Usuário Comum'):
                queryset = Solicitacao.objects.filter(
                    usuario__user=self.request.user.id)
            else:
                queryset = Solicitacao.objects.all()

            return queryset


class SistemaCrud(Crud):
    model = Sistema
    help_path = ''

    class CreateView(LoginRequiredMixin, crud.base.CrudCreateView):
        form_class = SistemaForm

    class UpdateView(LoginRequiredMixin, crud.base.CrudUpdateView):
        form_class = SistemaForm

    class ListView(LoginRequiredMixin, crud.base.CrudListView):
        pass
