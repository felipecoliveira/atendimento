import crud.base
from crud.base import Crud

from .forms import UsuarioExternoForm
from .models import UsuarioExterno


class UsuarioExternoCrud(Crud):
    model = UsuarioExterno
    help_path = ''

    class CreateView(crud.base.CrudCreateView):
        form_class = UsuarioExternoForm

    class UpdateView(crud.base.CrudUpdateView):
        form_class = UsuarioExternoForm
