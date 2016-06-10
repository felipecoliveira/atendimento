# -*- coding: utf-8 -*-
from __future__ import absolute_import
from braces.views import FormValidMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import DetailView, FormView

import crud.base
from atendimento.utils import str2bool
from crud.base import Crud

from .forms import (HabilitarEditForm, MudarSenhaForm, UsuarioEditForm,
                    UsuarioForm)
from .models import Usuario


class UsuarioCrud(Crud):
    model = Usuario
    help_path = u''

    class CreateView(crud.base.CrudCreateView):
        form_class = UsuarioForm
        form_valid_message = u'Cadastro realizado com sucesso. Aguarde a \
                              validação do seu perfil.'

        def get_success_url(self):
            return reverse(u'home')

    class ListView(LoginRequiredMixin, crud.base.CrudListView):
        pass

    class UpdateView(LoginRequiredMixin, crud.base.CrudUpdateView):
        form_class = UsuarioEditForm

        def get_initial(self):
            if self.get_object():

                tel1 = self.get_object().primeiro_telefone
                self.initial[u'primeiro_tipo'] = tel1.tipo
                self.initial[u'primeiro_ddd'] = tel1.ddd
                self.initial[u'primeiro_numero'] = tel1.numero
                self.initial[u'primeiro_principal'] = tel1.principal

                tel2 = self.get_object().segundo_telefone
                if tel2:
                    self.initial[u'segundo_tipo'] = tel2.tipo
                    self.initial[u'segundo_ddd'] = tel2.ddd
                    self.initial[u'segundo_numero'] = tel2.numero
                    self.initial[u'segundo_principal'] = tel2.principal

            return self.initial.copy()

        @property
        def layout_key(self):
            return u'UsuarioEdit'

    class DetailView(LoginRequiredMixin, crud.base.CrudDetailView):

        def get_context_data(self, **kwargs):
            context = super(DetailView, self).get_context_data(**kwargs)

            tel1 = context[u'object'].primeiro_telefone
            tel1 = [(u'Primeiro Telefone'),
                    (u'[%s] - %s' % (tel1.ddd, tel1.numero))]

            tel2 = context[u'object'].segundo_telefone or u''
            if tel2:
                tel2 = [(u'Segundo Telefone'),
                        (u'[%s] - %s' % (tel2.ddd, tel2.numero))]

            context[u'telefones'] = [tel1, tel2]
            return context

        @property
        def layout_key(self):
            return u'UsuarioDetail'

    class BaseMixin(crud.base.CrudBaseMixin):
        list_field_names = [u'username', u'nome_completo',
                            u'data_criacao', u'habilitado',
                            u'data_ultima_atualizacao']


class HabilitarDetailView(crud.base.CrudDetailView):
    template_name = u"usuarios/habilitar_detail.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context[u'pk'] = self.kwargs[u'pk']
        context[u'usuario'] = Usuario.objects.get(pk=self.kwargs[u'pk'])
        return self.render_to_response(context)


class HabilitarEditView(FormView):
    template_name = u"crud/form.html"

    def get(self, request, *args, **kwargs):
        context = {}

        usuario = Usuario.objects.get(pk=self.kwargs[u'pk'])
        form = HabilitarEditForm(instance=usuario)

        context[u'pk'] = self.kwargs[u'pk']
        context[u'form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = HabilitarEditForm(request.POST)
        usuario = Usuario.objects.get(pk=self.kwargs[u'pk'])
        usuario.habilitado = str2bool(form.data[u'habilitado'])
        usuario.data_ultima_atualizacao = timezone.now()

        usuario.save()
        return self.form_valid(form)

    def get_success_url(self):
        return reverse(u'usuarios:usuario_list')


class MudarSenhaView(FormValidMessageMixin, FormView):
    template_name = u"crud/form.html"
    form_class = MudarSenhaForm
    form_valid_message = u'Senha alterada com sucesso. É necessário fazer \
                             login novamente.'

    def get(self, request, *args, **kwargs):
        context = {}
        usuario = Usuario.objects.get(pk=self.kwargs[u'pk'])
        form = MudarSenhaForm(instance=usuario)
        context[u'pk'] = self.kwargs[u'pk']
        context[u'form'] = self.get_form()
        return self.render_to_response(context)

    def form_valid(self, form):
        usuario = Usuario.objects.get(pk=self.kwargs[u'pk'])
        u = usuario.user
        u.set_password(form.cleaned_data[u'password'])
        u.save()
        return super(MudarSenhaView, self).form_valid(form)

    def get_success_url(self):
        return reverse(u'home')
