import crud.base
from crud.base import Crud
from .models import UsuarioExterno
from .forms import UsuarioExternoForm


class UsuarioExternoCrud(Crud):
    model = UsuarioExterno
    help_path = ''

    class CreateView(crud.base.CrudCreateView):
        form_class = UsuarioExternoForm

    class UpdateView(crud.base.CrudUpdateView):
        form_class = UsuarioExternoForm

# def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
