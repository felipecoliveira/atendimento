from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import DetailView, FormView

import crud.base
from atendimento.utils import str2bool
from crud.base import Crud

from .forms import HabilitarEditForm, UsuarioEditForm, UsuarioForm
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

    class ListView(LoginRequiredMixin, crud.base.CrudListView):
        pass

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
        list_field_names = ['username', 'nome_completo',
                            'data_criacao', 'habilitado',
                            'data_ultima_atualizacao']


class HabilitarDetailView(LoginRequiredMixin, crud.base.CrudDetailView):
    template_name = "usuarios/habilitar_detail.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context['pk'] = self.kwargs['pk']
        context['usuario'] = Usuario.objects.get(pk=self.kwargs['pk'])
        return self.render_to_response(context)


class HabilitarEditView(LoginRequiredMixin, FormView):
    template_name = "crud/form.html"

    def get(self, request, *args, **kwargs):
        context = {}

        usuario = Usuario.objects.get(pk=self.kwargs['pk'])
        form = HabilitarEditForm(instance=usuario)

        context['pk'] = self.kwargs['pk']
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = HabilitarEditForm(request.POST)
        usuario = Usuario.objects.get(pk=self.kwargs['pk'])
        usuario.habilitado = str2bool(form.data['habilitado'])
        usuario.data_ultima_atualizacao = timezone.now()

        usuario.save()
        return self.form_valid(form)

    def get_success_url(self):
        return reverse('usuarios:usuario_list')
