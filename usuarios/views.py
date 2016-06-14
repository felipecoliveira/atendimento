from braces.views import FormValidMessageMixin
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import Permission, User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import FormView
from django.views.generic.edit import FormMixin

import crud.base
from atendimento.utils import str2bool
from crud.base import Crud

from .forms import (ConveniadoEditForm, MudarSenhaForm, ResponsavelEditForm,
                    UsuarioEditForm, UsuarioForm)
from .models import Usuario


class UsuarioCrud(Crud):
    model = Usuario
    help_path = ''

    class CreateView(crud.base.CrudCreateView):
        form_class = UsuarioForm
        form_valid_message = 'Cadastro realizado com sucesso. Aguarde a \
                              validação do seu perfil.'

        def get_success_url(self):
            return reverse('home')

    class UpdateView(LoginRequiredMixin, crud.base.CrudUpdateView):
        form_class = UsuarioEditForm

        def get_initial(self):
            if self.get_object():

                tel1 = self.get_object().primeiro_telefone
                self.initial['primeiro_tipo'] = tel1.tipo
                self.initial['primeiro_ddd'] = tel1.ddd
                self.initial['primeiro_numero'] = tel1.numero
                self.initial['primeiro_principal'] = tel1.principal

                tel2 = self.get_object().segundo_telefone
                if tel2:
                    self.initial['segundo_tipo'] = tel2.tipo
                    self.initial['segundo_ddd'] = tel2.ddd
                    self.initial['segundo_numero'] = tel2.numero
                    self.initial['segundo_principal'] = tel2.principal

            return self.initial.copy()

        @property
        def layout_key(self):
            return 'UsuarioEdit'

    class ListView(PermissionRequiredMixin, crud.base.CrudListView):

        def has_permission(self):
            if self.request.user.groups.filter(name='COPLAF'):
                perms = {'usuarios.can_change_conveniado'}
                return self.request.user.has_perms(perms)
            if self.request.user.groups.filter(name='COADFI'):
                perms = {'usuarios.can_change_responsavel'}
                return self.request.user.has_perms(perms)
            else:
                return False

    class DetailView(LoginRequiredMixin, crud.base.CrudDetailView):

        def get_context_data(self, **kwargs):
            context = super(DetailView, self).get_context_data(**kwargs)

            tel1 = context['object'].primeiro_telefone
            tel1 = [('Primeiro Telefone'),
                    ('[%s] - %s' % (tel1.ddd, tel1.numero))]

            tel2 = context['object'].segundo_telefone or ''
            if tel2:
                tel2 = [('Segundo Telefone'),
                        ('[%s] - %s' % (tel2.ddd, tel2.numero))]

            context['telefones'] = [tel1, tel2]
            return context

        @property
        def layout_key(self):
            return 'UsuarioDetail'

    class BaseMixin(crud.base.CrudBaseMixin):
        queryset = Usuario.objects.filter(habilitado=False)
        list_field_names = ['username', 'nome_completo',
                            'data_criacao', 'habilitado',
                            'data_ultima_atualizacao']


class ConveniadoView(PermissionRequiredMixin, FormView):
    template_name = "crud/form.html"
    permission_required = {'usuarios.change_usuario',
                           'usuarios.can_change_conveniado',
                           'usuarios.add_usuario'}

    def get(self, request, *args, **kwargs):
        context = {}

        usuario = Usuario.objects.get(pk=self.kwargs['pk'])
        form = ConveniadoEditForm(instance=usuario)

        context['pk'] = self.kwargs['pk']
        context['form'] = form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = ConveniadoEditForm(request.POST)
        usuario = Usuario.objects.get(pk=self.kwargs['pk'])
        if form.data.get('conveniado') == 'on':
            usuario.conveniado = True
        usuario.data_ultima_atualizacao = timezone.now()
        if usuario.conveniado is True and usuario.responsavel is True:
            usuario.habilitado = True
            user = User.objects.get(usuario__id=usuario.id)
            permissao = Permission.objects.get(
                name='Can add Solicitação de Novo Serviço')
            user.user_permissions.add(permissao)
        usuario.save()
        return self.form_valid(form)

    def get_success_url(self):
        return reverse('usuarios:usuario_list')


class ResponsavelView(PermissionRequiredMixin, FormView):
    template_name = "crud/form.html"
    permission_required = {'usuarios.change_usuario',
                           'usuarios.can_change_responsavel',
                           'usuarios.add_usuario'}

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return HttpResponseRedirect(reverse(
            'usuarios:conveniado_edit', kwargs={'pk': self.kwargs['pk']}))

    def get(self, request, *args, **kwargs):
        context = {}

        usuario = Usuario.objects.get(pk=self.kwargs['pk'])
        form = ResponsavelEditForm(instance=usuario)

        context['pk'] = self.kwargs['pk']
        context['form'] = form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = ResponsavelEditForm(request.POST)
        usuario = Usuario.objects.get(pk=self.kwargs['pk'])
        usuario.responsavel = str2bool(form.data['responsavel'])
        usuario.data_ultima_atualizacao = timezone.now()
        if usuario.conveniado is True and usuario.responsavel is True:
            usuario.habilitado = True
            user = usuario.user
            permissao = Permission.objects.get(
                name='Can add Solicitação de Novo Serviço')
            user.user_permissions.add(permissao)
        usuario.save()
        return self.form_valid(form)

    def get_success_url(self):
        return reverse('usuarios:usuario_list')


class MudarSenhaView(FormValidMessageMixin, FormView):
    template_name = "crud/form.html"
    form_class = MudarSenhaForm
    form_valid_message = 'Senha alterada com sucesso. É necessário fazer \
                             login novamente.'

    def get(self, request, *args, **kwargs):
        context = {}
        usuario = Usuario.objects.get(pk=self.kwargs['pk'])
        form = MudarSenhaForm(instance=usuario)
        context['pk'] = self.kwargs['pk']
        context['form'] = self.get_form()
        return self.render_to_response(context)

    def form_valid(self, form):
        usuario = Usuario.objects.get(pk=self.kwargs['pk'])
        u = usuario.user
        u.set_password(form.cleaned_data['password'])
        u.save()
        return super(MudarSenhaView, self).form_valid(form)

    def get_success_url(self):
        return reverse('home')
