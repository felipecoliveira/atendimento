import crud.base
from crud.base import Crud
import random

from .forms import SistemaForm, SolicitacaoEditForm, SolicitacaoForm
from .models import Sistema, Solicitacao

from usuarios.models import Usuario


class SolicitacaoCrud(Crud):
    model = Solicitacao
    help_path = ''

    class CreateView(crud.base.CrudCreateView):
        form_class = SolicitacaoForm

        def get_initial(self):
            usuario = Usuario.objects.get(user=self.request.user)
            initial = {'codigo': random.randint(0, 65500), 'usuario': usuario}
            return initial

    class UpdateView(crud.base.CrudUpdateView):
        form_class = SolicitacaoEditForm

        @property
        def layout_key(self):
            return 'SolicitacaoEdit'

    class ListView(crud.base.CrudListView):
        @property
        def layout_key(self):
            return 'SolicitacaoList'

class SistemaCrud(Crud):
    model = Sistema
    help_path = ''

    class CreateView(crud.base.CrudCreateView):
        form_class = SistemaForm

    class UpdateView(crud.base.CrudUpdateView):
        form_class = SistemaForm
