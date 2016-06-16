from braces.views import FormValidMessageMixin
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import DetailView, FormView, TemplateView
import crud.base
from django.core.mail import send_mail
from atendimento.utils import str2bool
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from crud.base import Crud

from .forms import (HabilitarEditForm, MudarSenhaForm, UsuarioEditForm,
                    UsuarioForm)
from .models import Usuario, ConfirmaEmail, User


class UsuarioCrud(Crud):
    model = Usuario
    help_path = ''

    class CreateView(crud.base.CrudCreateView):
        form_class = UsuarioForm
        form_valid_message = 'Cadastro realizado com sucesso. Aguarde a \
                              validação do seu perfil.'

        def get_success_url(self):
            kwargs = {}
            user = User.objects.get(email=self.request.POST.get('email'))
            confirmar_email = ConfirmaEmail(
                email=user.email,
                token=default_token_generator.make_token(user),
                user_id=urlsafe_base64_encode(force_bytes(user.pk)))
            confirmar_email.save()

            kwargs['token'] = confirmar_email.token
            kwargs['uidb64'] = confirmar_email.user_id
            assunto = "Cadastro no Sistema de Atendimento ao Usuário"
            full_url = self.request.get_raw_uri(),
            url_base = full_url[0][:full_url[0].find('usuario') - 1],
            mensagem = ("Este e-mail foi utilizado para fazer cadastro no " +
                        "Sistema de Atendimento ao Usuário do Interlegis.\n" +
                        "Caso você não tenha feito este cadastro, por favor " +
                        "ignore esta mensagem.\n" + url_base[0] +
                        reverse('usuarios:confirmar_email', kwargs=kwargs))
            remetente = settings.EMAIL_HOST_USER
            destinatario = [confirmar_email.email,
                            settings.EMAIL_HOST_USER]
            send_mail(assunto, mensagem, remetente, destinatario,
                      fail_silently=False)
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

        @property
        def layout_key(self):
            return 'UsuarioEdit'

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


class HabilitarDetailView(crud.base.CrudDetailView):
    template_name = "usuarios/habilitar_detail.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context['pk'] = self.kwargs['pk']
        context['usuario'] = Usuario.objects.get(pk=self.kwargs['pk'])
        return self.render_to_response(context)


class HabilitarEditView(FormView):
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


class ConfirmarEmailView(TemplateView):
    template_name = "usuarios/confirma_email.html"

    def get(self, request, *args, **kwargs):
        uid = urlsafe_base64_decode(self.kwargs['uidb64'])
        user = User.objects.get(id=uid)
        user.is_active = True
        user.save()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
