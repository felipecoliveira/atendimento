import random

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

import crud.base
from crud.base import Crud
from usuarios.models import Usuario

from .forms import SistemaForm, SolicitacaoEditForm, SolicitacaoForm
from .models import Sistema, Solicitacao


class SolicitacaoCrud(LoginRequiredMixin, Crud):
    model = Solicitacao
    help_path = ''

    class CreateView(PermissionRequiredMixin, crud.base.CrudCreateView):
        form_class = SolicitacaoForm
        permission_required = {'servicos.add_solicitacao'}

        def get_initial(self):
            if self.request.user.is_superuser:
                usuario = None
                self.initial['codigo'] = random.randint(0, 65500)
                self.initial['email_contato'] = usuario.email
                self.initial['telefone_contato'] = usuario.primeiro_telefone

            else:
                usuario = Usuario.objects.get(user=self.request.user)
                self.initial['usuario'] = usuario
                self.initial['codigo'] = random.randint(0, 65500)
                self.initial['email_contato'] = usuario.email
                self.initial['telefone_contato'] = usuario.primeiro_telefone

            return self.initial.copy()

    class UpdateView(PermissionRequiredMixin, crud.base.CrudUpdateView):
        form_class = SolicitacaoEditForm
        permission_required = {'servicos.change_solicitacao'}

        @property
        def layout_key(self):
            return 'SolicitacaoEdit'

        def get_initial(self):
            if self.request.user.is_superuser:
                return {'usuario': None,
                        'codigo': random.randint(0, 65500)}
            else:
                return {'usuario': Usuario.objects.get(
                    user=self.request.user.id),
                    'codigo': random.randint(0, 65500)}

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
