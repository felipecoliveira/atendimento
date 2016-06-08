from django.contrib.auth.models import Group, Permission


def cria_grupos_permissoes():
    Group.objects.create(name="Usuário Comum")
    Group.objects.create(name="COTIN")
    Group.objects.create(name="COADFI")
    Group.objects.create(name="COPLAF")

    cotin = Group.objects.get(name='COTIN')
    coplaf = Group.objects.get(name='COPLAF')
    coadfi = Group.objects.get(name='COADFI')

    permissao_add_usuario = Permission.objects.get(name="Can add Usuário")
    permissao_edit_usuario = Permission.objects.get(name="Can change Usuário")

    permissao_coplaf = Permission.objects.filter(
        name="Can change conveniado field")

    if permissao_coplaf:
        permissao_coplaf = permissao_coplaf[0]
    else:
        permissao_coplaf = Permission.objects.get(
            name="User can change habilitado field")

    permissao_coadfi = Permission.objects.get(
        name="User can change responsavel field")

    coplaf.permissions.add(permissao_add_usuario)
    coplaf.permissions.add(permissao_edit_usuario)
    coplaf.permissions.add(permissao_coplaf)

    coadfi.permissions.add(permissao_add_usuario)
    coadfi.permissions.add(permissao_edit_usuario)
    coadfi.permissions.add(permissao_coadfi)

    permissoes_cotin = Permission.objects.all()

    for p in permissoes_cotin:
        cotin.permissions.add(p)

if __name__ == '__main__':
    cria_grupos_permissoes()
