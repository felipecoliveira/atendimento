import crud.base
from crud.base import Crud
from django.core.urlresolvers import reverse
from .forms import UsuarioForm, UsuarioEditForm, HabilitarEditForm
from .models import Usuario
from django.views.generic.edit import FormMixin
from django.views.generic import UpdateView, FormView


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
        list_field_names = ['username', 'nome_completo',
                            'data_criacao', 'habilitado']


class HabilitarDetailView(crud.base.CrudDetailView):
    template_name = "usuarios/habilitar_detail.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context['pk'] = self.kwargs['pk']
        context['usuario'] = Usuario.objects.get(pk=self.kwargs['pk'])
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('usuarios:usuario_list')


class HabilitarEditView(FormView):
    template_name = "crud/form.html"

    def get(self, request, *args, **kwargs):
        form = HabilitarEditForm()
        context = {}
        context['pk'] = self.kwargs['pk']
        context['form'] = form
        return self.render_to_response(context)
