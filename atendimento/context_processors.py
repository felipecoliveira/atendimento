from usuarios.models import Usuario


def recupera_usuario(request):

    pk = request.user.pk
    if pk:
        return Usuario.objects.get(user_id=pk).pk
    else:
        return 0


def usuario_context(request):
    context = {'usuario_pk': recupera_usuario(request)}
    return context
