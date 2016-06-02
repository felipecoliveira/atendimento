import crud.base
from crud.base import Crud
from django.core.urlresolvers import reverse
from .forms import UsuarioForm, UsuarioEditForm
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

    class UpdateView(crud.base.CrudUpdateView):
        form_class = UsuarioEditForm

    class DetailView(crud.base.CrudDetailView):

        @property
        def layout_key(self):
            return 'UsuarioDetail'
