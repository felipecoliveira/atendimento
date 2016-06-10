from __future__ import absolute_import
import random

from django.contrib.auth.mixins import LoginRequiredMixin

import crud.base
from crud.base import Crud
from usuarios.models import Usuario

from .forms import SistemaForm, SolicitacaoEditForm, SolicitacaoForm
from .models import Sistema, Solicitacao


class SolicitacaoCrud(LoginRequiredMixin, Crud):
    model = Solicitacao
    help_path = u''

    class CreateView(LoginRequiredMixin, crud.base.CrudCreateView):
        form_class = SolicitacaoForm

        def get_initial(self):
            usuario = Usuario.objects.get(user=self.request.user)
            self.initial[u'usuario'] = usuario
            self.initial[u'codigo'] = random.randint(0, 65500)
            self.initial[u'email_contato'] = usuario.email
            self.initial[u'telefone_contato'] = usuario.primeiro_telefone
            return self.initial.copy()

    class UpdateView(LoginRequiredMixin, crud.base.CrudUpdateView):
        form_class = SolicitacaoEditForm

        @property
        def layout_key(self):
            return u'SolicitacaoEdit'

    class ListView(LoginRequiredMixin, crud.base.CrudListView):
        @property
        def layout_key(self):
            return u'SolicitacaoList'


class SistemaCrud(Crud):
    model = Sistema
    help_path = u''

    class CreateView(LoginRequiredMixin, crud.base.CrudCreateView):
        form_class = SistemaForm

    class UpdateView(LoginRequiredMixin, crud.base.CrudUpdateView):
        form_class = SistemaForm

    class ListView(LoginRequiredMixin, crud.base.CrudListView):
        pass
