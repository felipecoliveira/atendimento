import random

from django.contrib.auth.mixins import LoginRequiredMixin

import crud.base
from crud.base import Crud
from usuarios.models import Usuario

from .forms import SistemaForm, SolicitacaoEditForm, SolicitacaoForm
from .models import Sistema, Solicitacao


class SolicitacaoCrud(LoginRequiredMixin, Crud):
    model = Solicitacao
    help_path = ''

    class CreateView(LoginRequiredMixin, crud.base.CrudCreateView):
        form_class = SolicitacaoForm

        def get_initial(self):
            try:
                usuario = Usuario.objects.get(user=self.request.user)
                self.initial['usuario'] = usuario
                self.initial['codigo'] = random.randint(0, 65500)
                self.initial['email_contato'] = usuario.email
                self.initial['telefone_contato'] = usuario.primeiro_telefone
            except Usuario.DoesNotExist:
                pass
            return self.initial.copy() # TODO: por que?

    class UpdateView(LoginRequiredMixin, crud.base.CrudUpdateView):
        form_class = SolicitacaoEditForm

        @property
        def layout_key(self):
            return 'SolicitacaoEdit'

    class ListView(LoginRequiredMixin, crud.base.CrudListView):
        @property
        def layout_key(self):
            return 'SolicitacaoList'


class SistemaCrud(Crud):
    model = Sistema
    help_path = ''

    class CreateView(LoginRequiredMixin, crud.base.CrudCreateView):
        form_class = SistemaForm

    class UpdateView(LoginRequiredMixin, crud.base.CrudUpdateView):
        form_class = SistemaForm

    class ListView(LoginRequiredMixin, crud.base.CrudListView):
        pass
