import crud.base
from crud.base import Crud

from .forms import SistemaForm, TicketForm
from .models import Sistema, Ticket


class TicketCrud(Crud):
    model = Ticket
    help_path = ''

    class CreateView(crud.base.CrudCreateView):
        form_class = TicketForm

    class UpdateView(crud.base.CrudUpdateView):
        form_class = TicketForm


class SistemaCrud(Crud):
    model = Sistema
    help_path = ''

    class CreateView(crud.base.CrudCreateView):
        form_class = SistemaForm

    class UpdateView(crud.base.CrudUpdateView):
        form_class = SistemaForm
