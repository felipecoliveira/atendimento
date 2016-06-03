from django.utils import timezone
import crud.base
from crud.base import Crud, make_pagination
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django_filters.views import FilterView
from .forms import (ConveniadoEditForm, UsuarioForm,
                    UsuarioEditForm, ResponsavelEditForm,
                    HabilitadoFilterSet)
from .models import Usuario
from django.views.generic import FormView
from atendimento.utils import str2bool


class UsuarioCrud(Crud):
    model = Usuario
    help_path = ''

    class CreateView(crud.base.CrudCreateView):
        form_class = UsuarioForm
        form_valid_message = 'Cadastro realizado com sucesso. Aguarde a \
                              validação do seu perfil.'

        def get_success_url(self):
            return reverse('home')

    class UpdateView(crud.base.CrudUpdateView):
        form_class = UsuarioEditForm

    class DetailView(crud.base.CrudDetailView):

        @property
        def layout_key(self):
            return 'UsuarioDetail'

    class BaseMixin(crud.base.CrudBaseMixin):
        queryset = Usuario.objects.filter(habilitado=False)
        list_field_names = ['username', 'nome_completo',
                            'data_criacao', 'habilitado']

    def get_context_data(self, **kwargs):
        super(UsuarioCrud, self).get_context_data(**kwargs)
        import ipdb; ipdb.set_trace()

        if self.request.user.groups.filter(name='COADFI'):
            context = {
                'coadfi': True,
            }
            context.update(kwargs)
        if self.request.user.groups.filter(name='COPLAF'):
            context = {
                'coplaf': True,
            }
        context.update(kwargs)

        return context


class HabilitarDetailView(crud.base.CrudDetailView):
    template_name = "usuarios/habilitar_detail.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context['pk'] = self.kwargs['pk']
        context['usuario'] = Usuario.objects.get(pk=self.kwargs['pk'])
        return self.render_to_response(context)


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
        # import ipdb; ipdb.set_trace()
        form = ConveniadoEditForm(request.POST)
        usuario = Usuario.objects.get(pk=self.kwargs['pk'])
        if form.data.get('conveniado') == 'on':
            usuario.conveniado = True
        usuario.data_ultima_atualizacao = timezone.now()
        if usuario.conveniado is True and usuario.responsavel is True:
            usuario.habilitado = True
        usuario.save()
        return self.form_valid(form)

    def get_success_url(self):
        return reverse('usuarios:usuario_list')


class ResponsavelView(PermissionRequiredMixin, FormView):
    template_name = "crud/form.html"
    permission_required = {'usuarios.change_usuario',
                           'usuarios.can_change_responsavel',
                           'usuarios.add_usuario'}

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
        usuario.save()
        return self.form_valid(form)

    def get_success_url(self):
        return reverse('usuarios:usuario_list')


def redireciona(user):
    if user.has